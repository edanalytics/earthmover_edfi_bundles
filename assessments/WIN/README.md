* **Title**: WIN - API 3.X
* **Description**: This template maps WIN Academic Skills and Soft Skills results files. 
* **API version**: 5.2
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/WIN_results.csv</code></summary>
This bundle was written using a single state's results file format as a guide. It may require
updates for different states if these files are significantly different.

</details>

Or use the sample file (`data/sample_anonymized_file.csv`).


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Default column is 'StudentID'
- EDFI_DS_VERSION: The Ed-Fi data standard major version for your ODS. Integer only; supported versions are 3, 4, and 5

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"STUDENT_ID_NAME": "StateID",
"EDFI_DS_VERSION": "4" }'
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