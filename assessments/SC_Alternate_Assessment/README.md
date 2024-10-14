* **Title**: South Carolina Alternate Assessments (SC-Alt)
* **Description**: This template is for the South Carolina Alternate Assessments

* **API version**: 5.2
* **Submitter name**: Keen Zarate
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- API_YEAR: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2022-2023, enter `2023`
- INPUT_FILE: The path to the SC-ALT .csv file you want to transform


### Examples
Running a SC ALT file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/sc_alt.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023"}'
```


Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"EDFI_API_YEAR": yourAPIYear }'
```
