* **Title**: ACCUPLACER Placement Tests - API 3.X
* **Description**: This template maps College Board Next-Generation ACCUPLACER files. It currently handles the placement tests only. It may be extended in the future to map ESL and Essay tests.
* **API version**: 5.2
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/accuplacer.csv</code></summary>
This template will only work with the ACCUPLACER placement test results file.
</details>

Or use the sample file (data/sample_anonymized_file.csv).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped
- API_YEAR: The API year of the ODS for which we would send these records
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is 'Student ID' from the ACCUPLACER file.

### Examples
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"API_YEAR": "2024",
"STUDENT_ID_NAME": "Student ID" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```