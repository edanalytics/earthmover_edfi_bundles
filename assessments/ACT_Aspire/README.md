* **Title**: ACT Aspire Bundle -API 3.x
* **Description**: This bundle includes the ACT Asprie assessment which is a summative assessment, designed to measure student progress across multiple subject areas towards meeting college reasiness bendhmarks. 
* **API version**: 5.3
* **Submitter name**: SA Salter
* **Submitter organization**: Crocus LLC

To run this bundle, please add your own source file data/ACT_Aspire_Sample_File.csv

This bundle was designed to work with the ACT 2015 Aspire Summative Student Performance File Format layout provided by the assessment vendor. 

## Running this bundle without Student ID Xwalking
To run this bundle without implementing the student ID xwalking packages:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file.csv",
"OUTPUT_DIR": "output/" 
}'
```

## CLI Parameters

# Required
* OUTPUT_DIR: Where output files will be written
* INPUT_FILE: The assessment file to be mapped
* STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Can be one of the native columns in the assessment file (e.g., State Student ID) when the bundle is run directly. Otherwise leave the default value edFi_studentUniqueID
* POSSIBLE_STUDENT_ID_COLUMNS: This should contain all the possible native student id columns in the assessment file( e.g., State Student ID) .

# Optional
* DESCRIPTOR_NAMESPACE: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor. The default value is: uri://ed-fi.org

## Run Earthmover
Using an ID column from the assessment file:
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/ACT_Aspire_Sample_2015.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "State Student ID"
}'

## Lightbeam
Once you have inspected the output JSONL for issues, check the settings in lightbeam.yaml and transmit them to your Ed-Fi API with:
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```
