This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Curriculum Associates i-Ready Diagnostic Math and ELA Assessments - API 3.X
* **Description**: This template includes the i-Ready Diagnostic Math and ELA Assessments. It requires the standard vendor file export format.
* **API version**: 5.2
* **Submitter name**: Ryan Aguilar
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/CA_i-Ready.csv</code></summary>
This bundle works with the standard i-Ready Diagnostic Math and ELA Assessments vendor file exports.

</details>

Or use one of the sample files (`data/sample_anonymized_file_ela.csv` or `data/sample_anonymized_file_math.csv`).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The assessment file to be mapped
- INPUT_FILETYPE: Specify the input filetype. Defaults to csv
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Defaults to `Student ID`.

### Examples
```bash
earthmover run -c earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file_ela.csv",
"OUTPUT_DIR": "./output/",
"STUDENT_ID_NAME": "Student ID"}'
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