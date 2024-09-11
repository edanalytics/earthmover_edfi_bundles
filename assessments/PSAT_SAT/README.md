This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: PSAT/SAT Results - API 3.X
* **Description**: This template includes the SAT, PSAT/NMSQT, PSAT 10, and PSAT 8/9 assessments. 
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/Student_Data_File.csv</code></summary>
This bundle currently works with SAT, PSAT/NMSQT, PSAT 10, and PSAT 8/9 files in the format provided by College Board. It is compatible with both the pencil and paper tests (~2016-2023) and newer digital tests (2024 and beyond).

</details>

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped
- API_YEAR: The API year of the ODS for which we would send these records
- TEST_TYPE: Identifies which assessment is being loaded from the current input file. Must be `SAT`, `PSAT/NMSQT`, `PSAT 10`, or `PSAT 8/9`.
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is `STATE_STUDENT_ID` from the results file.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file_sat.csv",
"API_YEAR": "2023",
"TEST_TYPE": "SAT",
"STUDENT_ID_NAME": "STATE_STUDENT_ID" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "youAPIYear",
"BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
