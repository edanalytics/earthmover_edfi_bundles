* **Title**: STAAR Interim - API 3.X
* **Description**: This template covers STAAR Interim Data File Format (from standard Cambium extracts)

* **API version**: 5.2
* **Submitter name**: Rob Little
* **Submitter organization**: Education Analytics


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- API_YEAR: The Ed-Fi API year that the output of this template will send to. e.g. for school year 2022-2023, enter `2023`
- INPUT_FILE: The path to the STAAR Summative .csv file you want to transform


### Optional

If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `from` and ID included in the assessment file and `to` the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_FROM: Declare which column in the assessment file should be used for the crosswalk join

When using an ID xwalk, set `STUDENT_ID_NAME` as `to`.

### Examples
Running a STAAR Interim file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/staar_interim.csv",
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


(**Above**: a graphical depiction of the dataflow.)
