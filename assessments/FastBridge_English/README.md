## FastBridge English (Early Reading)

* **Title:** FastBridge English Early Reading Assessment Results
* **Description:** This template maps FastBridge English Early Reading Assessment Results, providing comprehensive evaluation of various reading skills including decodable words, letter names, letter sounds, nonsense words, sentence reading, and sight words. The bundle includes pre-processing to pivot season-based columns into student assessment rows, handle growth metrics, and map positional error columns.
* **API version:** 5.3
* **Submitter name:** Bruk Woldearegay
* **Submitter organization:** Crocus LLC.

To run this bundle, please add your own source file(s) and column(s):
<details>
This template works with vendor layout file structure. See the sample anonymized file for reference.

The input CSV should contain:
- Student demographic columns (Local ID, State ID, First Name, Last Name, etc.)
- Season-specific assessment columns (e.g., "Fall Early Reading English Final Date", "Winter Decodable Words WRC per minute")
- Growth columns (e.g., "Decodable Words from Fall to Winter")
- Generic "Error" columns positioned after objective anchor columns
</details>

Sample file: `data/Sample_earlyReading_deidentified.csv`

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
"INPUT_FILE": "data/Sample_earlyReading_deidentified.csv",
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