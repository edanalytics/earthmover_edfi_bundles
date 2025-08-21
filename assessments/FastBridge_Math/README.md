## FastBridge Math (Early Math)

* **Title:** FastBridge Math Early Math Assessment Results
* **Description:** This template maps FastBridge Math Early Math Assessment Results, providing comprehensive evaluation of various mathematical skills including composing, counting objects, decomposing, equal partitioning, match quantity, number sequence, numeral identification, place value, quantity discrimination, subitizing, verbal addition, verbal subtraction, and story problems. The bundle includes pre-processing to pivot season-based columns into student assessment rows, handle growth metrics, and map positional error columns.
* **API version:** 5.3
* **Submitter name:** Bruk Woldearegay
* **Submitter organization:** Crocus LLC.

To run this bundle, please add your own source file(s) and column(s):
<details>
This template works with vendor layout file structure. The pre-execute script transforms the wide CSV format (seasons as columns) into a long format (seasons as rows) suitable for Ed-Fi ingestion. See the sample anonymized file.
</details>

Sample file: `data/Sample_FastBridge_earlyMath_2023_2024_deidentified.csv`

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Where to store the earthmover runs.csv file
- **INPUT_FILE**: The student assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Default column is the 'StateID' from the vendor layout file.
- **SCHOOL_YEAR**: The year of the assessment file (format as 'YYYY' e.g. '2024', etc).

### Examples

**Step 1: Running the pre-execute script to transform the file structure**
The FastBridge Math CSV comes in a wide format with seasons as columns. The pre-execute script pivots this into a long format and handles growth metrics and error column mapping:

```python
fast_bridge_math_pre_exec(source_file, output_file)
```

Example:
```python
fast_bridge_math_pre_exec(
    'data/Sample_FastBridge_earlyMath_2023_2024_deidentified.csv',
    'data/Sample_FastBridge_earlyMath_2023_2024_deidentified_pivoted.csv'
)
```

**Step 2: Running earthmover with the transformed file:**
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "data/Sample_FastBridge_earlyMath_2023_2024_deidentified_pivoted.csv",
"OUTPUT_DIR": "output/",
"STUDENT_ID_NAME": "State ID",
"SCHOOL_YEAR": "2024"}'
```

### Pre-Execute Script Features

The pre-execute script (`python_pre_exec/pre-execute.py`) performs the following transformations:

1. **Season Pivoting**: Converts wide format (seasons as columns) to long format (seasons as rows)
2. **Growth Metrics Processing**: Handles growth columns (e.g., "Composing from Fall to Winter") and pivots them based on ending season
3. **Error Column Mapping**: Maps generic "Error" columns to objective-specific error fields using positional anchors (IC per minute, NRC per minute)
4. **Column Normalization**: Converts all column names to snake_case format for consistency
5. **Data Validation**: Filters out empty rows and ensures data quality

### Error Column Handling

The script automatically detects and maps generic "Error" columns that appear positionally after anchor metrics:
- Generic columns named "Error", "Error.1", "Error.2", etc.
- Maps to objective-specific names like "numeral_identification_one_error", "numeral_identification_kg_error"
- Uses "IC per minute" and "NRC per minute" columns as anchors to determine which objective each error belongs to

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"STATE_DIR": "./tmp/.lightbeam/",
"EDFI_API_BASE_URL": "<yourURL>",
"EDFI_API_CLIENT_ID": "<yourID>",
"EDFI_API_CLIENT_SECRET": "<yourSecret>",
"SCHOOL_YEAR": "<yourAPIYear>"}'
```


### Output Structure

After transformation, the pivoted file will contain:
- One row per student per season with assessment data
- Snake_case column names for consistency
- Growth metrics attached to records based on ending season
- Mapped error columns with objective-specific names (e.g., `numeral_identification_one_error`, `numeral_identification_kg_error`)

