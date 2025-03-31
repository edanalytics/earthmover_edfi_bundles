* **Title**: STAAR Summative - API 3.X
* **Description**: This template covers STAAR Summative Data File Formats for:
    * Grades 3-8 Reporting Data File (compatibility from 21-22 to 24-25)
    * Alternate 2 Grades 3-8 Data File (compatibility from 21-22 to 24-25)
    * End-of-Course Reporting Data File (compatibility from 21-22 to 24-25)
    * Alternate 2 End-of-Course Reporting Data File (compatibility from 21-22 to 24-25)
      
For more info on these data files, including the File Format documentation, see https://tea.texas.gov/student-assessment/testing/student-assessment-overview/data-file-formats

Note, there is a separate earthmover.yaml file for each of the 4 reporting data formats, but they are all included in this bundle, because the `/templates/` files work on all four formats (the json files will share the same structure).

* **API version**: 5.2
* **Submitter name**: Rob Little
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- `API_YEAR`: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2022-2023, enter `2023`
- (During `run` only) `INPUT_FILE`: The path to the STAAR Summative .csv file you want to transform
- (During `deps` only) `FORMAT`: One of the four supported file formats: `['Standard', 'Alternate', 'End-of-Course', 'End-of-Course Alternate']`

In order to run the bundle for a specific format, you must use `earthmover deps` to load the corresponding configuration.

### Examples
Running a STAAR Summative 3-8 file:
```bash
earthmover deps -c ./earthmover.yaml -p '{
"API_YEAR": "2023",
"FORMAT": "Standard"
}'

earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file__standard.csv",
"STUDENT_ID_NAME": "tx_unique_student_id",
"FORMAT": "Standard",
"API_YEAR": "2023"
}'
```
Running a STAAR Summative EOC ALT file:
```bash
earthmover deps -c ./earthmover.yaml -p '{
"API_YEAR": "2023",
"FORMAT": "End-of-Course Alternate"
}'

earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "path/to/staar_summative_eoc_alt_2023.csv",
"FORMAT": "End-of-Course Alternate",
"API_YEAR": "2023"
}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"EDFI_API_YEAR": yourAPIYear }'
```

