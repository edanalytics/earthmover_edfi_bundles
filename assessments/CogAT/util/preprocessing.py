import sys
import pandas as pd

# HOW TO USE
# python preprocess.py path_to_fwf_file path_to_format_file
# Example:
# python preprocessing.py "../data/Data Export Winter 24.txt" cogat_format.csv

file_format = pd.read_csv(sys.argv[2])
filepath = sys.argv[1]
colnames = file_format.column_name
colspecs = list(zip(file_format.start_index,file_format.end_index))

# The file doesn't have headers by default, so header should be None.
# But pandas was consistently incorrectly parsing only the first line,
# so I added an extra newline at the beginning of the file and set header=0.
# This is not ideal and should be investigated :)
df = pd.read_fwf(filepath, header=0, names=colnames, colspecs=colspecs)
df.to_csv(filepath.replace(".txt", ".csv"), index=False)
print(df)