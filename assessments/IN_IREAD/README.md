This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Indiana IREAD-3 - API 3.X
* **Description**: This template includes IREAD-3 subjects ELA, Math, Social Studies, Science, Biology, US Government.
* **API version**: 7.1
* **Submitter name**: Na Nguyen
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/IREAD-3.csv</code></summary>
This bundle currently works with IREAD-3 scores as exported from CRS, as of SY 2024.  It has not yet been updated for the new Checkpoints format that is being piloted for SY 2025.  

</details>

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped 
- API_YEAR: The API year of the ODS for which we would send these records

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -f -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv"
}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "youAPIYear",
"BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```

### Notes
- This assessment is created and administered by the state of Indiana, and is only ever expected to be used within Indiana.

### Reference
Here is a complete list of columns provided by the export

- Student_First_Name
- Student_Last_Name
- STN
- Student_DOB
- Gender
- Ethnicity
- Special_Education_Status
- Identified_English_Learner_Status
- Section_504_Status
- Free/Reduced_Price_Meals
- Enrolled_Grade
- Enrolled_School
- Enrolled_School_ID
- Enrolled_Corporation
- Enrolled_Corporation_ID
- Test_name
- Overall_scale_score
- Overall_proficiency_level
- IREAD-3_Reported_Lexile_Measure
- IREAD-3_Reported_Quantile_Measure
- IREAD-3_Passing_Status
- IREAD-3_Grade_2_Passing_Status
- IREAD-3_Overall_scale_score
- IREAD-3_Grade_2_Overall_scale_score
- IREAD-3_Reported_Lexile_Measure
- IREAD-3_Grade_2_Reported_Lexile_Measure
- IREAD-3_Reporting_Category_1_Performance
- IREAD-3_Reporting_Category_2_Performance
- IREAD-3_Reporting_Category_3_Performance
- Test Start Date
- Test Completion Date
