This is an earthmover bundle for mapping generic local assessment data to Ed-Fi.

This bundle is designed to be flexible — it accepts any assessment data that has a student ID, assessment name, test date, and score.

To run this bundle, please add your own source file(s):
* <code>data/your_assessment_file.csv</code>

Or use the sample file (`data/sample_anonymized_file.csv`).

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The assessment results file to be mapped
### Optional
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Default is 'edFi_studentUniqueID'
- POSSIBLE_STUDENT_ID_COLUMNS: Comma-separated list of possible student ID columns. Default is 'StudentID'
- INPUT_FILETYPE: File type of the input file (csv or tsv). Default is 'csv'
- DESCRIPTOR_NAMESPACE: Namespace for Ed-Fi descriptors. Default is 'uri://ed-fi.org'

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c earthmover.yaml -p '{
"INPUT_FILE": "data/sample_anonymized_file.csv",
"STATE_FILE": "./runs.csv",
"OUTPUT_DIR": "output/",
"STUDENT_ID_NAME": "StudentID"
}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"API_YEAR": "yourAPIYear",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
