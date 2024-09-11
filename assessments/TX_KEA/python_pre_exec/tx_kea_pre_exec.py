import pandas as pd
import csv
import re
import os


def tx_kea_pre_exec(
        input_file_path,
        output_file_path):
    """
    Process a TX-KEA CSV file's column headers, saving a new file with fixed column headers (combining the sparse headers from row 1 with headers in row 3)

    EXAMPLE:
    Input File:
    |         | LETTERS       |              | SCREENER     |             |               |              |
    |---------|---------------|--------------|--------------|-------------|---------------|--------------|
    |         |               |              |              |             |               |              |
    | student | letters_score | letters_date | shapes_score | shapes_date | letters_score | letters_date |
    | 100     | 5             | 3/24         | 8            | 3/24        | 5             | 3/24         |

    Pre-processed Output File:
    | student | LETTERS__letters_score | LETTERS__letters_date | SCREENER__shapes_score | SCREENER__shapes_date | SCREENER__letters_score | SCREENER__letters_date |
    |---------|------------------------|-----------------------|------------------------|-----------------------|-------------------------|------------------------|
    | 100     | 5                      | 3/24                  | 8                      | 3/24                  | 5                       | 3/24                   |

    Args:
        input_file_path (str): Path to the input CSV file.
        output_file_path (str): Path to save the processed CSV file.

    Returns:
        output_file_path
    """
    # Read headers and remove BOM
    with open(input_file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = [next(reader) for _ in range(3)]

    if headers[2][0] != 'Wave':
        print("Returning None so downstream skips: File header format is unexpected. First column on 3rd row should be labeled 'Wave'.")
        return None

    # Process headers to get long headers
    long_headers = pd.DataFrame({
        'col_i': [idx for row in headers for idx, value in enumerate(row)],
        'value': [value.replace(' ', '_').upper() if value != '' else None for row in headers for value in row],
        'row_i': [row_i for row_i, row in enumerate(headers) for _ in row]
    })

    # Fill NA values
    long_headers['value'] = long_headers['value'].ffill()

    # Reshape long headers to wide headers
    wide_headers = pd.pivot_table(long_headers, values='value', index='col_i', columns='row_i', aggfunc='first').reset_index()

    # Concatenate column names with separator '__'
    wide_headers['concat_colname'] = wide_headers[[0, 2]].apply(lambda x: '__'.join(x.dropna().astype(str)), axis=1)

    # Remove leading and trailing underscores
    wide_headers['concat_colname'] = wide_headers['concat_colname'].apply(lambda x: re.sub('^_+|_+$', '', x))

    # Read full file
    full_file = pd.read_csv(input_file_path, skiprows=3, names=wide_headers['concat_colname'], dtype=str)

    # Save full file to output path
    # create dir (works if there is a file name or not)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    full_file.to_csv(output_file_path,
            header=True,
            index=False)
    
    # TODO fix dynamic task mapping so that we don't need to pass these through, and can just return the output path
    return(output_file_path)
