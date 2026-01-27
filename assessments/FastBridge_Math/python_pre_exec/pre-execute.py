import re
import pandas as pd

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_snake_pat = re.compile(r'[^0-9a-zA-Z]')
_growth_pat = re.compile(r'(.+?)\s+from\s+(.+?)\s+to\s+(.+?)(?:\.(\d+))?$', re.IGNORECASE)

def to_snake_case(text):
    """Convert arbitrary text to snake_case."""
    text = _snake_pat.sub('_', text)
    return re.sub(r'_+', '_', text).strip('_').lower()

# ---------------------------------------------------------------------------
# FastBridge transformer (seasons → rows, sub-assessments → columns)
# ---------------------------------------------------------------------------
def fast_bridge_math_pre_exec(source_file, output_file):
    """Transform a FastBridge Early Math wide CSV into season-long rows.

    Args:
        source_file: Path to the original wide CSV (values preserved as strings).
        output_file: Path where the season-long CSV will be written.

    Returns:
        The final transformed DataFrame that has been written to output_file.
    """

    # Step 1: Load input (as strings) and normalize whitespace in headers
    df = pd.read_csv(source_file, dtype=str)
    df.columns = [re.sub(r"\s+", " ", col.strip()) for col in df.columns]

    # Step 2: Define base student/entity columns and ensure presence
    base_cols = [
        "Assessment", "Assessment Language", "State", "District", "School",
        "Local ID", "State ID", "FAST ID", "First Name", "Last Name",
        "Gender", "DOB", "Race", "Special Ed. Status", "Grade",
    ]
    # Step 3: Identify growth columns and build mapping to clean names and end seasons
    growth_columns = []
    growth_mappings = {}
    for col in df.columns:
        m = _growth_pat.search(col)
        if m and "from" in col.lower() and "to" in col.lower():
            metric_name = m.group(1).strip()
            start_season = m.group(2).strip()
            end_season = m.group(3).strip()

            clean_metric = to_snake_case(metric_name)
            clean_start = to_snake_case(start_season)
            clean_name = f"{clean_metric}_from_{clean_start}"

            growth_columns.append(col)
            growth_mappings[col] = {
                "clean_name": clean_name,
                "end_season": end_season,
                "start_season": start_season,
            }

    # Step 4: Discover seasons from headers
    seasons = sorted(
        {
            col.replace(" Early Math Final Date", "").strip()
            for col in df.columns
            if "Early Math Final Date" in col
        }
    )

    # Precompute per-season score columns (non-growth, non-date)
    season_score_cols = {}
    season_score_snake = {}
    for season in seasons:
        prefix = f"{season} "
        cols = [
            c
            for c in df.columns
            if c.startswith(prefix)
            and "Final Date" not in c
            and c not in growth_columns
            and c not in base_cols
        ]
        season_score_cols[season] = cols
        season_score_snake[season] = {c: to_snake_case(c[len(prefix) :]) for c in cols}

    # Map positional generic Error columns to objective-specific names.
    # Some files include repeated generic columns named "Error" (possibly suffixed: Error, Error.1, ...)
    # that belong to the preceding objective (usually the column ending with "IC per minute" or
    # "WRC per minute"). We detect and map these to canonical headers: "{season} {objective} Error".
    error_mapping = {}
    for season in seasons:
        season_prefix = f"{season} "
        for i, col in enumerate(df.columns):
            if not col.startswith(season_prefix):
                continue
            anchor_suffix = None
            # Math files use different anchors than English; include NRC per minute

            if col.endswith(" IC per minute"):
                anchor_suffix = " IC per minute"
            elif col.endswith(" NRC per minute"):
                anchor_suffix = " NRC per minute"
            if anchor_suffix is None:
                continue
            # derive objective between season prefix and anchor suffix
            objective = col[len(season_prefix) : -len(anchor_suffix)]
            # next column is a generic Error column? map it
            if i + 1 < len(df.columns):
                next_col = df.columns[i + 1]
                if next_col.startswith("Error") and not next_col.startswith(season_prefix):
                    error_mapping[next_col] = f"{season} {objective} Error"

    # Step 5: Build growth pivot table
    growth_pivot_data = None
    if growth_columns:
        print(f"Processing {len(growth_columns)} growth columns…")
        by_end_clean = {}
        for orig_col, info in growth_mappings.items():
            by_end_clean.setdefault(info["end_season"], {}).setdefault(info["clean_name"], []).append(orig_col)

        end_seasons = sorted(by_end_clean.keys())
        print(f"End seasons found: {end_seasons}")

        growth_base_df = df[base_cols].copy()
        growth_rows = []
        for idx in growth_base_df.index:
            base_vals = growth_base_df.loc[idx].to_dict()
            for end_season in end_seasons:
                pivot_row = dict(base_vals)
                pivot_row["Season"] = end_season
                for clean_name, orig_cols in by_end_clean[end_season].items():
                    final_value = None
                    for oc in orig_cols:
                        val = df.at[idx, oc]
                        if pd.notna(val) and str(val).strip() != "":
                            final_value = val
                            break
                    pivot_row[clean_name] = final_value
                growth_rows.append(pivot_row)

        growth_pivot_data = pd.DataFrame(growth_rows)
        print(f"Created growth pivot data with shape: {growth_pivot_data.shape}")

        gp_cols = [c for c in growth_pivot_data.columns if "_from_" in c]
        if gp_cols:
            has_growth = growth_pivot_data[gp_cols].notna() & (growth_pivot_data[gp_cols] != "")
            growth_pivot_data = growth_pivot_data[has_growth.any(axis=1)]
            print(f"After filtering empty growth rows: {growth_pivot_data.shape}")

    # Step 6: Build assessment rows per season
    assessment_rows = []
    final_date_col_of = {s: f"{s} Early Math Final Date" for s in seasons}
    for idx in df.index:
        row = df.loc[idx]
        for season in seasons:
            fdate_col = final_date_col_of[season]
            if fdate_col not in df.columns:
                continue
            final_date = row.get(fdate_col)
            if pd.isna(final_date) or str(final_date).strip() == "":
                continue
            season_row = {c: row.get(c) for c in base_cols}
            season_row["Season"] = season
            season_row["Final_Date"] = final_date
            for col in season_score_cols[season]:
                snake_name = season_score_snake[season][col]
                season_row[snake_name] = row.get(col)
            # include mapped generic Error columns for this season
            season_prefix = f"{season} "
            for orig_err, mapped_hdr in error_mapping.items():
                if mapped_hdr.startswith(season_prefix):
                    obj = mapped_hdr[len(season_prefix):].replace(" Error", "")
                    snake_err = to_snake_case(f"{obj} error")
                    season_row[snake_err] = row.get(orig_err)
            assessment_rows.append(season_row)

    assessment_df = pd.DataFrame(assessment_rows)
    if not assessment_df.empty:
        score_cols = [c for c in assessment_df.columns if c not in base_cols + ["Season", "Final_Date"]]
        if score_cols:
            has_scores = assessment_df[score_cols].notna() & (assessment_df[score_cols] != "")
            assessment_df = assessment_df[has_scores.any(axis=1)]

    print(f"Created assessment data with shape: {assessment_df.shape}")
    if not assessment_df.empty:
        print("Assessment score columns:", [c for c in assessment_df.columns if c not in base_cols + ["Season", "Final_Date"]])
    else:
        print("No assessment data found")

    # Step 7: Merge growth onto assessment
    if growth_pivot_data is not None:
        print(f"Assessment data shape: {assessment_df.shape}")
        print(f"Growth data shape: {growth_pivot_data.shape}")
        merge_cols = base_cols + ["Season"]
        final_df = pd.merge(assessment_df, growth_pivot_data, on=merge_cols, how="left")
        print(f"Final merged data shape: {final_df.shape}")
    else:
        final_df = assessment_df

    # Step 8: Write output
    final_df.to_csv(output_file, index=False)
    return final_df
