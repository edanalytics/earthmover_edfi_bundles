* **Title**: STAAR Summative - API 3.X
* **Description**: This template covers STAAR Summative Data File Formats for:
    * Grades 3-8 Reporting Data File (21-22 and 22-23 compatible)
    * Alternate 2 Grades 3-8 Data File (21-22 and 22-23 compatible)
    * End-of-Course Reporting Data File (21-22 and 22-23 compatible)
    * Alternate 2 End-of-Course Reporting Data File (21-22 and 22-23 compatible)
      
For more info on these data files, including the File Format documentation, see https://tea.texas.gov/student-assessment/testing/student-assessment-overview/data-file-formats

Note, there is a separate earthmover.yaml file for each of the 4 reporting data formats, but they are all included in this bundle, because the `/templates/` files work on all four formats (the json files will share the same structure).

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
Running a STAAR Summative 3-8 file:
```bash
earthmover run -c ./earthmover_staar_summative.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"STUDENT_ID_NAME": "tx_unique_student_id",
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"API_YEAR": "2023"}'
```
Running a STAAR Summative EOC ALT file:
```bash
earthmover run -c ./earthmover_staar_summative_eoc_alt.yaml -p '{
"INPUT_FILE": "path/to/staar_summative_eoc_alt_2023.csv",
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
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

