* **Title**: Kindergarten Readiness Assessment (KRA) - API 3.X
* **Description**: This template includes the KRA assessments, designed to measure individual readiness across various domains.
* **API version**: 5.3
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file<code>data/KRA_Data_File.csv</code>

This bundle works with KRA files in the format provided by the assessment vendor. 

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `PS_StudentID`, `StudentSUNS`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `PS_StudentID`, `StudentSUNS` ) . 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor . The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c earthmover.yaml -p '{
"INPUT_FILE": "data/KRA_sample_file_deidentified.csv",
"STATE_FILE": "./runs.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_NAME": "PS_StudentID",
}'
```

Once you have inspected the output JSONL for issues, check the settings in lightbeam.yaml and transmit them to your Ed-Fi API with:

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "DATA_DIR": "./output/",
  "API_YEAR": "yourAPIYear",
  "BASE_URL": "yourURL",
  "EDFI_API_CLIENT_ID": "yourID",
  "EDFI_API_CLIENT_SECRET": "yourSecret"
}'
```