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

    # build one rename map
    rename_map = {}
    for season, sa in product(seasons, sub_assessments):
        prefix = f'{season} {sa} '
        score_cols = df.filter(regex=fr'^{re.escape(prefix)}(?!.*Final Date)').columns
        for col in score_cols:
            metric = col[len(prefix):]
            rename_map[col] = to_snake_case(f'{sa} {metric}')

        fdate_col = f'{season} {sa} Final Date'
        if sa != 'Early Reading English' and fdate_col in df.columns:
            rename_map[fdate_col] = to_snake_case(f'{sa} final_date')

    df = df.rename(columns=rename_map)

    # explode seasons
    tmp = (
        df.assign(_k=1)
          .merge(pd.DataFrame({'Season': seasons, '_k': 1}), on='_k')
          .drop('_k', axis=1)
    )

    # Use the exact column name as it appears after cleaning
    def get_final_date(row):
        season_col = f"{row.Season} Early Reading English Final Date"
        # Check if the column exists, if not return empty string
        return row.get(season_col, '')

    tmp['Final_Date'] = tmp.apply(get_final_date, axis=1)

    score_cols = tmp.columns.difference(base_cols + ['Season', 'Final_Date'])

    # Fix the filtering logic to properly exclude NaN and empty values
    mask = (
        tmp['Final_Date'].notna() &  # Not NaN
        (tmp['Final_Date'] != '') &  # Not empty string
        tmp[score_cols].notna().any(axis=1)  # Has some score data
    )

    final_df = tmp.loc[
        mask, list(base_cols) + ['Season', 'Final_Date'] + list(score_cols)
    ]

    final_df.to_csv(output_file, index=False)
    return final_df
