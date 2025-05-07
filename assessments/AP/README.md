* **Title**: Advanced Placement (AP) - API 3.X
* **Description**: This template includes the AP exams, designed to measure college readiness across different subjects.
* **API version**: 7.1
* **Submitter name**: SA Salter
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file<code>data/SAMPLE_AP_2324.csv</code>

This bundle works with AP files in the format provided by the assessment vendor. 

## CLI Parameters

### Examples

There is a pre executing python function that needs to be run before running earthmover to vertically stack the results. The pre-execution step is created to resolve performance issues when using earthmover: 
```bash
python -c'import python_pre_exec.ap_pre_exec; ap_pre_exec(input_file="./data/SAMPLE_AP_2324.csv", output_file="./data/SAMPLE_AP_processed.csv")'
```
The earthmover processes the output file from the pre-execution step that takes in the vendor file as input. 
### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `studentId`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `studentId`) . 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor . The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/SAMPLE_AP_processed.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "studentId"
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