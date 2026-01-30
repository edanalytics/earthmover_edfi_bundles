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

Sample file: `data/Sample_earlyMath_deidentified.csv`

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Where to store the earthmover runs.csv file
- **INPUT_FILE**: The student assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Default column is the 'StateID' from the vendor layout file.
- **API_YEAR**: The year of the assessment file (format as 'YYYY' e.g. '2024', etc).

### Examples

Running earthmover: 
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "data/Sample_earlyMath_deidentified_pivoted.csv",
"OUTPUT_DIR": "output/",
"STUDENT_ID_NAME": "State ID",
"API_YEAR": "2024"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"STATE_DIR": "./tmp/.lightbeam/",
"EDFI_API_BASE_URL": "<yourURL>",
"EDFI_API_CLIENT_ID": "<yourID>",
"EDFI_API_CLIENT_SECRET": "<yourSecret>",
"API_YEAR": "<yourAPIYear>"}'
```