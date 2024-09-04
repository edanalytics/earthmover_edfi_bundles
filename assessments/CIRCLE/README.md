This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: CIRCLE Progress Monitoring System (PreK) Assessment Results - API 3.X
* **Description**: This template maps CLI CIRCLE Assessment Results, providing a comprehensive evaluation of student's progress through various learning domains crucial for academic success.
    
    For more info on these data files, see https://public.cliengage.org/tools/assessment/circle-progress-monitoring/

* **API version**: 5.3
* **Submitter name**: Angelica Lastra
* **Submitter organization**: Education Analytics

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written.
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives.
- INPUT_FILE: The path to the CLI CIRCLE .csv file you want to transform.

### Examples
Running a CLI Circle file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"STUDENT_ID_NAME": "Student_State_ID",
"STATE_FILE": "./runs.csv",
"OUTPUT_DIR": "./output"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"EDFI_API_YEAR": yourAPIYear }'
```