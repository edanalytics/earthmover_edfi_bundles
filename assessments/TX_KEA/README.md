This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Texas Kindergarten Entry Assessment (TX-KEA) Assessment Results - API 3.X
* **Description**: This template maps CLI TX-KEA Assessment Results, providing a comprehensive evaluation of various learning domains crucial for academic success at kindergarten entry and throughout the kindergarten year.
    
    For more info on these data files, see https://public.cliengage.org/tools/assessment/tx-kea/

* **API version**: 5.3
* **Submitter name**: Angelica Lastra
* **Submitter organization**: Education Analytics

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written.
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives.
- INPUT_FILE: The path to the CLI TX-KEA .csv file you want to transform.

### Examples

Fixing the file headers BEFORE running earthmover: 
```bash
python -c'import python_pre_exec.tx_kea_pre_exec; tx_kea_pre_exec(input_file_path="./data/sample_anonymized_file.csv", output_file_path="./data/sample_anonymized_file_fixed_headers.csv")'
```


Running a CLI TX-KEA file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file_fixed_headers.csv",
"STUDENT_ID_NAME": "STUDENT_STATE_ID",
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