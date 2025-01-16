* **Title**:  Developmental Indicators for the Assessment of Learning, Fourth Edition (DIAL-4) - API 3.X
* **Description**: This template includes the DIAL-4 assessment, designed to identify young children who need further testing or who need help with
academic skills. The DIAL-4 tests a child’s motor skills (skipping, jumping, cutting, writing), conceptual skills (knowledge
of colors, counting), and language skills (knowledge of letters and words, ability to solve problems).
* **API version**: 5.3
* **Submitter name**: Mariela Suárez
* **Submitter organization**: CrocusLLC

To run this bundle, please add your own source file<code>data/DIAL4_SAMPLE_data_file.csv</code>

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `suns`, `student_number`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `suns`, `student_number`). 
- **SCHOOL_ID**: Which column to use as the Ed-Fi `schoolId`. Can be one of the native columns in the assessment file (e.g., `schoolcode`, `districtcode`) when the bundle is run directly.
- **POSSIBLE_SCHOOL_ID_COLUMNS**: This should contain all the possible school id columns in the assessment file( e.g., `schoolcode`, `districtcode`). 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor. The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "./data/sample_anonymized_file.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "suns",
  "SCHOOL_ID":"schoolcode"
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