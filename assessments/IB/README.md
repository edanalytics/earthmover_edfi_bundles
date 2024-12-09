This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: International Baccalaureate (IB) Results - API 3.X
* **Description**: This template maps International Baccalaureate assessment results.
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/ib.csv</code></summary>
This template will only work with the standard IB results file.
</details>

Or use the sample file (data/sample_anonymized_file.csv).

## Note on Student IDs
The IB results file does not include student IDs besides internal IB candidate IDs. This bundle expects a column called `student_unique_id` to be present in the results file, which will need to be added and populated as a pre-preprocessing step before this bundle can be used.

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the IB .csv file you want to transform
- API_YEAR: The API year that the output of this template will be sent to
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is `student_unique_id`, which must be added to the file

### Examples
Running earthmover for an IB file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"API_YEAR": "2024",
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