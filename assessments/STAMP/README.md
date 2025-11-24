* **Title**: STAndards-based Measurement of Proficiency (STAMP) - API 3.X
* **Description**: This template includes the STAMP assessments, designed to measure language proficiency across various languages.
* **API version**: 7.1
* **Submitter name**: SA Salter
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file<code>data/STAMP_Data_File.csv</code>

This bundle works with STAMP 4S, STAMP WS, STAMP Monolingual, STAMP Latin and STAMP ASL (Partially since data files do not have fields for expressive and receptive) files in the format provided by the assessment vendor. For details about the mapping look at the [mapping document](./mapping.md) found here.

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `Test Taker ID`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `Test Taker ID`) . 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor . The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/STAMP_deidentified_sample_file.csv",
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"STUDENT_ID_NAME": "Test Taker ID"
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