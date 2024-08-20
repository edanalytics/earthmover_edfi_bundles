This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: International Baccalaureate (IB) Results - API 3.X
* **Description**: This template maps International Baccalaureate assessment results.
* **API version**: 5.3
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

## Note on Student IDs
The IB results file does not include student IDs besides internal IB candidate IDs. This bundle expects a column called `student_unique_id` to be present in the results file, which will need to be added and populated as a pre-preprocessing step before this bundle can be used.

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written.
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the IB .csv file you want to transform.
- API_YEAR: The API year that the output of this template will be sent to.

### Examples
Running earthmover for an IB file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"API_YEAR": "2024" }'
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