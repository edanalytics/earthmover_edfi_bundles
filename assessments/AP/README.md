This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Advanced Placement (AP) - API 3.X
* **Description**: This template includes the AP exams, designed to measure college readiness across different subjects.
* **API version**: 7.1
* **Submitter name**: SA Salter
* **Submitter organization**: CrocusLLC

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/SAMPLE_AP_2324.csv</code></summary>
This bundle works with AP files in the wide format provided by College Board, containing up to 30 exam slots and 6 award slots per student.

</details>

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped
- API_YEAR: The API year of the ODS for which we would send these records
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is `studentId` (renamed from `Student Identifier` during processing). Leave as default `edFi_studentUniqueID` when using the student ID xwalk package.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/SAMPLE_AP_2324.csv",
"API_YEAR": "2024",
"STUDENT_ID_NAME": "studentId" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "yourAPIYear",
"BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
