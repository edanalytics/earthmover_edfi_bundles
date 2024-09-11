* **Title**: STAAR Interim - API 3.X
* **Description**: This template covers STAAR Interim Data File Format (from standard Cambium extracts)

* **API version**: 5.2
* **Submitter name**: Rob Little
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- API_YEAR: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2022-2023, enter `2023`
- INPUT_FILE: The path to the STAAR Summative .csv file you want to transform
- STATE_FILE: Where to store the earthmover runs.csv file



### Examples
Running a STAAR Interim file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"STUDENT_ID_NAME": "TSDS UID",
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
