This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Colorado Measures of Academic Success (CMAS) Assessment Results - API 3.X
* **Description**: This template includes the CMAS Mathematics, Science, English Language Arts/Literacy, and Spanish Language Arts/Literacy assessments. 
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/co_csa_cmas_Math_ELA_District_Student_Data_File.csv</code></summary>


</details>

then run the following command:
```bash
earthmover run -c ./CMAS_EdFi_3_2/earthmover.yaml -p '{
"BUNDLE_DIR": "./CMAS_EdFi_3_2/",
"INPUT_FILE": "./CMAS_EdFi_3_2/data/co_csa_cmas_Math_ELA_District_Student_Data_File.csv",
"OUTPUT_DIR": "./CMAS_EdFi_3_2/output" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c CMAS_EdFi_3_2/lightbeam.yaml -p '{
"DATA_DIR": "./CMAS_EdFi_3_2/output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```

![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)