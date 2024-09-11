This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: WIDA ACCESS for ELLs Assessment Results - API 3.X
* **Description**: This template includes the WIDA ACCESS Summative and WIDA Alternate ACCESS assessment results. 
* **API version**: 5.3
* **Submitter name**: Susan Xiong
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
* <code>data/ACCESS_Results_File.csv</code>

then run the following command:
```bash
earthmover run -c earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file_ACCESS.csv",
"OUTPUT_DIR": "output",
"STUDENT_ID_NAME": "StateStudentID",
"SCHOOL_YEAR" : "2024",
"ALTERNATE": "N" }'
```

Runtime notes:
- If you are processing an ACCESS file from 2021 or earlier, use `-c earthmover_2021.yaml`.
- The <code>ALTERNATE</code> parameter must be set to "Y" for Alternate results files and "N" for Summative/Standard files.

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c lightbeam.yaml -p '{
"DATA_DIR": "output/",
"API_YEAR": "2024",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
