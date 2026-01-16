## FastBridge CBMmath

* **Title:** FastBridge CBMmath
* **Description**: This template maps FastBridge CBMmath Automaticity, Process, and Concepts & Applications (CAP) assessment results. This covers the comprehensive screening version of the assessment, not the progress monitoring version. 
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/fastbridge_cbmm_{type}.csv</code></summary>
This template will only work with the vendor-provided FastBridge files. Be sure to specify the correct TEST_TYPE variable for your file.
</details>

Or use a sample file (data/sample_anonymized_file_cbmm_auto.csv).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the FastBridge Early Reading - Spanish .csv file you want to transform
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId
- API_YEAR: The school year associated with the results file
- TEST_TYPE: Auto, Process, or CAP

### Examples
Running earthmover:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "output/" ,
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file_cbmm_auto.csv",
"STUDENT_ID_NAME": "Local ID",
"API_YEAR": "2023",
"TEST_TYPE": "Auto" 
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