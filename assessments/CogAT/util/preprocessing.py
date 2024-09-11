# Loads CogAT FWF data into memory and parses it into a dataframe
#
# The print statements at the bottom are a quality check ensuring that no rows
# are incorrectly filtered out.
#
## HOW TO USE
# python preprocess.py path_to_fwf_file path_to_format_file
# Example:
# python preprocessing.py "../data/Data Export Winter 24.txt" cogat_format.csv

from io import StringIO
import os
import sys
from pathlib import Path

import pandas as pd

# Pandas is able to read fixed-width data directly from a text file. However,
#   we found that it reads the first row incorrectly when doing this. We ensure
#   correct behavior by loading the data into memory first
filepath = sys.argv[1]
raw = Path(filepath).read_text(encoding="utf-8-sig")
raw_no_blank_lines = os.linesep.join([s for s in raw.splitlines() if s.strip()])

file_format = pd.read_csv(sys.argv[2])
colnames = file_format.column_name
colspecs = list(zip(file_format.start_index, file_format.end_index))
df = pd.read_fwf(
    StringIO(raw_no_blank_lines),
    header=None,
    names=colnames,
    colspecs=colspecs,
    # if we don't do this, read_fwf strips leading whitespaces - 'delimiter' is kind of a
    #    misnomer and the default value is " ". When leading spaces are removed, all values
    #    in score columns become misaligned
    # ref: https://stackoverflow.com/questions/57012437/pandas-read-fwf-removes-white-space
    delimiter="\n\t",
    # if we don't cast to string, columns that contain a string of flags (e.g. "0000100")
    #    will be read in as integers and written as "100"
    converters={c: str.rstrip for c in colnames},
)

df.to_csv(os.path.join(os.getcwd(), f"{Path(filepath).stem}.csv"), index=False)
print(df)

print(f"Raw FWF raws: {len(raw.split(os.linesep))}")
print(f"Non-blank rows: {len(raw_no_blank_lines.split(os.linesep))}")
print(f"CSV rows: {len(df.index)}")
