* **Title**:  Phonological Awareness Literacy Screening (PALS) - API 3.X
* **Description**: This template includes the PALS assessments, designed to measure children's literacy skills and helps identify students who may need additional instruction.
* **API version**: 5.3
* **Submitter name**: Mariela Suárez
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file<code>data/PALS_SAMPLE_data_file.csv</code>

This bundle works with PALS files in the format provided by the assessment vendor. For details about the mapping look at the [mapping document](./mapping.md) found here.

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `STD_STI`, `ID`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `STD_STI`, `ID` ) . 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor . The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/PALS_SAMPLE_data_file.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "STD_STI"
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