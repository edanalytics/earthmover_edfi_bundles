This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Cambridge International AS & A Levels Results - API 3.X
* **Description**: This template maps Cambridge International assessment results.
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/cambridge.csv</code></summary>
This template will only work with the vendor specification of the Cambridge results file. See `data/sample_anonymized_file.csv` for column names.
</details>

Or use the sample file (data/sample_anonymized_file.csv).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the ASVAB .csv file you want to transform
- SCHOOL_YEAR: The school year associated with the results file
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId
- EDFI_DS_VERSION: The Ed-Fi data standard major version for your ODS. Integer only; supported versions are 3, 4, and 5

### Examples
Running earthmover for a Cambridge file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"SCHOOL_YEAR": "2025",
"STUDENT_ID_NAME": "STUDENT_STATE_ID",
"EDFI_DS_VERSION": 3 }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": yourAPIYear }'
```