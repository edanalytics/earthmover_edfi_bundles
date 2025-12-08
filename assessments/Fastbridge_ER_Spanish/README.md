## FastBridge Early Reading - Spanish

* **Title:** FastBridge Early Reading - Spanish
* **Description**: This template maps FastBridge Early Reading - Spanish assessment results. This covers the comprehensive screening version of the assessment, not the progress monitoring version. 
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/fastbridge_er_spanish.csv</code></summary>
This template will only work with the vendor-provided FastBridge Early Reading - Spanish results file.
</details>

Or use the sample file (data/sample_anonymized_file_fastbridge_er_spanish.csv).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the FastBridge Early Reading - Spanish .csv file you want to transform
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId
- SCHOOL_YEAR: The school year associated with the results file
- EDFI_DS_VERSION: The Ed-Fi data standard major version for your ODS. Integer only; supported versions are 3, 4, and 5

### Examples
Running earthmover for an ASVAB file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "output/" ,
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file_fastbridge_er_spanish.csv",
"STUDENT_ID_NAME": "Local ID",
"SCHOOL_YEAR": "2024",
"EDFI_DS_VERSION": "4"
}'
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