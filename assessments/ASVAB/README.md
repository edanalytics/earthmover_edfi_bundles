This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Armed Services Vocational Aptitude Battery (ASVAB) Results - API 3.X
* **Description**: This template maps ASVAB assessment results.
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/asvab.csv</code></summary>
This template will only work with the vendor-provided ASVAB results file.
</details>

Or use the sample file (data/sample_anonymized_file.csv).

## Note on Student IDs
The ASVAB results file does not include student IDs. This bundle expects a column called `student_unique_id` to be present in the results file, which will need to be added and populated as a pre-preprocessing step before this bundle can be used.

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the ASVAB .csv file you want to transform
- API_YEAR: The API year that the output of this template will be sent to
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is `student_unique_id`, which must be added to the file

### Examples
Running earthmover for an ASVAB file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"SCHOOL_YEAR": "2024",
"STUDENT_ID_NAME": "student_unique_id" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"EDFI_API_YEAR": yourAPIYear }'
```