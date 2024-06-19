Title: ACT Assessment Results
Description: American College Test Assessment Results
API version: 5.3
Submitter name: Ludmila Janda
Submitter organization: Education Analytics

To run this bundle, please add your own source file(s) and column(s):

### Required
- OUTPUT_DIR: Where output files will be written.
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives.
- INPUT_FILE: The path to the ACT .csv file you want to transform.

### Examples
Running an ACT file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/ACT.csv",
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