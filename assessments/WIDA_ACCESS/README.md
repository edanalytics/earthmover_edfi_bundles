This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: WIDA ACCESS for ELLs Assessment Results - API 3.X
* **Description**: This template includes the WIDA ACCESS Summative and WIDA Alternate ACCESS assessment results. 
* **API version**: 5.3
* **Submitter name**: Susan Xiong
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
* <code>data/ACCESS_Results_File.csv</code>

then run the following command, noting that the <code>ALTERNATE</code> parameter must be set to Y for Alternate results files and N for Summative files. <code>STUDENT_ID_NAME</code> will be "StateStudentID" or "District Student ID" depending on which field is used for <code>student_unique_id</code> in Ed-Fi:
```bash
earthmover run -c earthmover.yml -p '{
"BUNDLE_DIR": ".",
"ACCESS_RESULTS_FILE": "data/ACCESS_Results_File.csv",
"OUTPUT_DIR": "output",
"STUDENT_ID_NAME": "StateStudentID",
"SCHOOL_YEAR" : "2024",
"ALTERNATE": "N" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c lightbeam.yml -p '{
"DATA_DIR": "output/",
"API_YEAR": "2024",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
