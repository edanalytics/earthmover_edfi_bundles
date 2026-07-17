* **Title**: South Carolina Alternate Assessments (SC-Alt)
* **Description**: This template is for the South Carolina Alternate Assessments

* **API version**: 5.2
* **Submitter name**: Keen Zarate
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- API_YEAR: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2023-2024, enter `2024`
- INPUT_FILE: The path to the SC-ALT .csv file you want to transform


### Examples
Running a SC ALT file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file_2024.csv",
"OUTPUT_DIR": "output/",
"API_YEAR": "2024",
"STUDENT_ID_NAME": "StateID"}'
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
