* **Title**: STAAR Summative - API 3.X
* **Description**: This template covers STAAR Summative Data File Formats for:
    * Grades 3-8 Reporting Data File
    * Alternate 2 Grades 3-8 Data File
    * End-of-Course Reporting Data File
    * Alternate 2 End-of-Course Reporting Data File
For more info on these data files, including the File Format documentation, see https://tea.texas.gov/student-assessment/testing/student-assessment-overview/data-file-formats
* **API version**: 5.2
* **Submitter name**: Rob Little
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- API_YEAR: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2022-2023, enter `2023`


### Optional
Note, you can enter any combination of these parameters, depending on the files you have. If you have e.g. a 3-8 file AND an Alternate EOC file, both will be converted to a common .json structure and saved in one studentAssessments.json file
- STAAR_SUMMATIVE_INPUT_FILE: The path to a "Grades 3-8 Reporting Data File"
- STAAR_SUMMATIVE_ALT_INPUT_FILE: The path to a "Alternate 2 Grades 3-8 Data File"
- STAAR_SUMMATIVE_EOC_INPUT_FILE: The path to a "End-of-Course Reporting Data File"
- STAAR_SUMMATIVE_EOC_ALT_INPUT_FILE: The path to a "Alternate 2 End-of-Course Reporting Data File"

If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `from` and ID included in the assessment file and `to` the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_JOIN_COLUMN: Declare which column in the assessment file should be used for the crosswalk join

When using an ID xwalk, set `STUDENT_ID_NAME` as `to`.

### Examples
Running a single 3-8 file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"STAAR_SUMMATIVE_INPUT_FILE": "path/to/staar_summative_3-8_2023.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023"}'
```

Running all four files (note, they will be stacked together into one output file):
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"STAAR_SUMMATIVE_INPUT_FILE": "path/to/staar_summative_3-8_2023.csv",
"STAAR_SUMMATIVE_ALT_INPUT_FILE": "path/to/staar_summative_3-8_ALT2_2023.csv",
"STAAR_SUMMATIVE_EOC_INPUT_FILE": "path/to/staar_summative_EOC_2023.csv",
"STAAR_SUMMATIVE_EOC_ALT_INPUT_FILE": "path/to/staar_summative_EOC_ALT2_2023.csv",
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

![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)