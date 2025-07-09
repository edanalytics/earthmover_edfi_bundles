import re
import pandas as pd

def to_snake_case(text: str) -> str:
    text = re.sub(r'[^0-9a-zA-Z]', '_', text)
    return re.sub(r'_+', '_', text).strip('_').lower()

def fast_bridge_english_pre_exec(source_file: str,
                                      output_file: str,
                                      validation: bool = True) -> pd.DataFrame:
    if validation:
        print("Loading data…")
    df = pd.read_csv(source_file)

    base_cols = [
        'Assessment', 'Assessment Language', 'State', 'District', 'School',
        'Local ID', 'State ID', 'FAST ID', 'First Name', 'Last Name',
        'Gender', 'DOB', 'Race', 'Special Ed. Status', 'Grade'
    ]

    seasons = sorted({
        col.replace(' Early Reading English Final Date', '').strip()
        for col in df.columns if 'Early Reading English Final Date' in col
    })

    sub_assessments = sorted({
        col.split(' ', 1)[1].replace(' Final Date', '')
        for col in df.columns
        if any(col.startswith(f'{s} ') and ' Final Date' in col for s in seasons)
    })

    season_frames = []
    for season in seasons:
        season_df = df[base_cols].copy()
        season_df['Season'] = season
        season_df['Final_Date'] = df.get(
            f'{season} Early Reading English Final Date', ''
        )

        for sa in sub_assessments:
            score_cols = [
                c for c in df.columns
                if c.startswith(f'{season} {sa} ') and 'Final Date' not in c
            ]
            for col in score_cols:
                new_name = to_snake_case(
                    f"{sa} {col.replace(f'{season} {sa} ', '')}"
                )
                season_df[new_name] = df[col]

            fcol = f'{season} {sa} Final Date'
            if sa != 'Early Reading English' and fcol in df.columns:
                season_df[to_snake_case(f'{sa} final_date')] = df[fcol]

        season_frames.append(season_df)

    combined = pd.concat(season_frames, ignore_index=True)

    score_cols = [
        c for c in combined.columns
        if c not in base_cols + ['Season', 'Final_Date']
    ]
    mask = combined['Final_Date'].astype(bool) & combined[score_cols].notna().any(axis=1)
    final_df = combined.loc[mask].copy()
    final_df = final_df[base_cols + ['Season', 'Final_Date'] + score_cols]

    final_df.to_csv(output_file, index=False)

    if validation:
        print(f"Saved {len(final_df):,} rows → {output_file}")

    return final_df
