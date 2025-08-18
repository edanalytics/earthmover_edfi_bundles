import re
import pandas as pd
from itertools import product

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_snake_pat = re.compile(r'[^0-9a-zA-Z]')
def to_snake_case(text: str) -> str:
    """Convert to snake_case quickly."""
    text = _snake_pat.sub('_', text)
    return re.sub(r'_+', '_', text).strip('_').lower()

# ---------------------------------------------------------------------------
# FastBridge transformer (seasons → rows, sub-assessments → columns)
# ---------------------------------------------------------------------------
def fast_bridge_english_pre_exec(source_file: str,
                                 output_file: str) -> pd.DataFrame:

    df = pd.read_csv(source_file, dtype=str)          # read once, keep as str

    # Clean up column names - fix extra spaces (e.g., "Summer  " -> "Summer")
    df.columns = [re.sub(r'\s+', ' ', col.strip()) for col in df.columns]

    base_cols = [
        'Assessment', 'Assessment Language', 'State', 'District', 'School',
        'Local ID', 'State ID', 'FAST ID', 'First Name', 'Last Name',
        'Gender', 'DOB', 'Race', 'Special Ed. Status', 'Grade'
    ]

    # Identify and separate growth columns
    growth_columns = []
    growth_mappings = {}  # original_col -> {clean_name, end_season, start_season}

    for col in df.columns:
        # Match patterns like 'Growth Score from Fall to Winter' and variations with suffixes
        match = re.search(r'(.+?)\s+from\s+(.+?)\s+to\s+(.+?)(?:\.(\d+))?$', col, re.IGNORECASE)
        if match and 'from' in col.lower() and 'to' in col.lower():
            metric_name = match.group(1).strip()  # e.g., "Growth Score"
            start_season = match.group(2).strip()  # e.g., "Fall"
            end_season = match.group(3).strip()   # e.g., "Winter"

            # Create clean column name with source season: metric_from_season
            clean_metric = to_snake_case(metric_name)
            clean_start_season = to_snake_case(start_season)
            clean_name = f"{clean_metric}_from_{clean_start_season}"

            growth_columns.append(col)
            growth_mappings[col] = {
                'clean_name': clean_name,
                'end_season': end_season,
                'start_season': start_season
            }

    # discover seasons & sub-assessments
    seasons = sorted({
        col.replace(' Early Reading English Final Date', '').strip()
        for col in df.columns if 'Early Reading English Final Date' in col
    })

    sub_assessments = sorted({
        col.split(' ', 1)[1].replace(' Final Date', '')
        for col in df.columns
        if any(col.startswith(f'{s} ') and ' Final Date' in col for s in seasons)
    })

    # Create growth pivot data separately
    growth_pivot_data = None
    if growth_columns:
        print(f"Processing {len(growth_columns)} growth columns...")

        # Create base data for growth pivot (just the base columns)
        growth_base_df = df[base_cols].copy()

        # Create growth pivot rows - one row per student per end season
        growth_rows = []

        # Get all unique end seasons from growth columns
        end_seasons = sorted(set(info['end_season'] for info in growth_mappings.values()))
        print(f"End seasons found: {end_seasons}")

        for idx, row in growth_base_df.iterrows():
            for end_season in end_seasons:
                # Create a row for this student and end season
                pivot_row = row.to_dict()
                pivot_row['Season'] = end_season

                # Group original columns by clean name to handle duplicates
                columns_by_clean_name = {}
                for orig_col, info in growth_mappings.items():
                    if info['end_season'] == end_season:
                        clean_name = info['clean_name']
                        if clean_name not in columns_by_clean_name:
                            columns_by_clean_name[clean_name] = []
                        columns_by_clean_name[clean_name].append(orig_col)

                # For each clean column name, consolidate values from duplicate columns
                for clean_name, orig_cols in columns_by_clean_name.items():
                    # Take the first non-null, non-empty value from the duplicate columns
                    final_value = None
                    for orig_col in orig_cols:
                        value = df.iloc[idx][orig_col]
                        if pd.notna(value) and str(value).strip() != '':
                            final_value = value
                            break

                    pivot_row[clean_name] = final_value

                growth_rows.append(pivot_row)

        growth_pivot_data = pd.DataFrame(growth_rows)
        print(f"Created growth pivot data with shape: {growth_pivot_data.shape}")

        # Filter out rows with no growth values
        growth_cols = [col for col in growth_pivot_data.columns if '_from_' in col]
        if growth_cols:
            # Keep rows that have at least one non-null, non-empty growth value
            has_growth_data = growth_pivot_data[growth_cols].notna() & (growth_pivot_data[growth_cols] != '')
            growth_mask = has_growth_data.any(axis=1)
            growth_pivot_data = growth_pivot_data[growth_mask]
            print(f"After filtering empty growth rows: {growth_pivot_data.shape}")

    # build one rename map for non-growth columns
    rename_map = {}
    for season, sa in product(seasons, sub_assessments):
        prefix = f'{season} {sa} '
        score_cols = df.filter(regex=fr'^{re.escape(prefix)}(?!.*Final Date)').columns
        # Exclude growth columns from normal processing
        score_cols = [col for col in score_cols if col not in growth_columns]
        for col in score_cols:
            metric = col[len(prefix):]
            rename_map[col] = to_snake_case(f'{sa} {metric}')

        fdate_col = f'{season} {sa} Final Date'
        if sa != 'Early Reading English' and fdate_col in df.columns:
            rename_map[fdate_col] = to_snake_case(f'{sa} final_date')

    # Filter out growth columns before renaming
    non_growth_df = df.drop(columns=growth_columns)
    non_growth_df = non_growth_df.rename(columns=rename_map)

    # Create season-specific assessment rows (similar to growth data approach)
    assessment_rows = []

    for idx, row in df.iterrows():  # Use original df, not non_growth_df which has columns removed
        for season in seasons:
            # Check if this student has data for this season
            final_date_col = f'{season} Early Reading English Final Date'
            if final_date_col not in df.columns:
                continue

            final_date = row[final_date_col]
            if pd.isna(final_date) or str(final_date).strip() == '':
                continue

            # Create row for this student-season combination
            season_row = {col: row[col] for col in base_cols}
            season_row['Season'] = season
            season_row['Final_Date'] = final_date

            # Add only season-specific assessment scores
            for col in df.columns:
                if col in base_cols or col == final_date_col or col in growth_columns:
                    continue

                # Check if this column belongs to the current season
                if col.startswith(f'{season} '):
                    # Extract the metric part and create snake_case name
                    metric_part = col[len(f'{season} '):]
                    # Skip Final Date columns as we already handle them
                    if 'Final Date' in metric_part:
                        continue
                    snake_name = to_snake_case(metric_part)
                    season_row[snake_name] = row[col]

            assessment_rows.append(season_row)

    assessment_df = pd.DataFrame(assessment_rows)

    # Filter to keep only rows with actual assessment score data
    if len(assessment_df) > 0:
        score_cols = [col for col in assessment_df.columns
                     if col not in base_cols + ['Season', 'Final_Date']]
        if score_cols:
            # Keep rows that have at least one non-null, non-empty score
            has_score_data = assessment_df[score_cols].notna() & (assessment_df[score_cols] != '')
            score_mask = has_score_data.any(axis=1)
            assessment_df = assessment_df[score_mask]

    print(f"Created assessment data with shape: {assessment_df.shape}")
    if len(assessment_df) > 0:
        print(f"Assessment score columns: {[col for col in assessment_df.columns if col not in base_cols + ['Season', 'Final_Date']]}")
    else:
        print("No assessment data found")

    # Join growth data with assessment data if available
    if growth_pivot_data is not None:
        print(f"Assessment data shape: {assessment_df.shape}")
        print(f"Growth data shape: {growth_pivot_data.shape}")

        # Merge on base columns + Season
        merge_cols = base_cols + ['Season']
        final_df = pd.merge(
            assessment_df,
            growth_pivot_data,
            on=merge_cols,
            how='left'  # Only keep rows that exist in assessment_df (which are already filtered)
        )
        print(f"Final merged data shape: {final_df.shape}")
    else:
        final_df = assessment_df

    final_df.to_csv(output_file, index=False)
    return final_df
