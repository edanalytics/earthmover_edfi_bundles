This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Colorado Measures of Academic Success (CMAS) Assessment Results - API 3.X
* **Description**: This template includes the CMAS Mathematics, Science, English Language Arts/Literacy, and Spanish Language Arts/Literacy assessments. 
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/cmas_Student_Data_File.csv</code></summary>


</details>

then run the following command, noting that the <code>SCIENCE</code> parameter must be set to Y for science results files:
```bash
earthmover run -c ./CMAS/earthmover.yaml -p '{
"BUNDLE_DIR": "./CMAS/",
"INPUT_FILE": "./CMAS/data/cmas_Student_Data_File.csv",
"OUTPUT_DIR": "./CMAS/output",
"SCIENCE": "N" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c CMAS/lightbeam.yaml -p '{
"DATA_DIR": "./CMAS/output/",
"API_YEAR": "2023",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
