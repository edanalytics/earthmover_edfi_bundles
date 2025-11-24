* **Title**: myIGDIs Assessment Bundle - API 3.X
* **Description**: This template includes the myIGDIs assessments, designed to measure individual growth and development indicators across various domains.
* **API version**: 7.1
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC

To run this bundle, please add your own source file `data/myIGDIs_Data_File.csv`

This bundle works with myIGDIs files in the format provided by the assessment vendor. 
## CLI Parameters

### Required

- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `Student Id`) when the bundle is run directly. Otherwise, leave the default value `edFi_studentUniqueID`
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student ID columns in the assessment file (e.g., `Student Id`)

### Optional

- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as `ResultDatatypeTypeDescriptor`. The default value is: `uri://ed-fi.org`

### Examples

### Examples

There is a pre executing python function that needs to be run before running earthmover to vertically stack the results. The pre-execution step is created to resolve performance issues when using earthmover: 
```bash
python -c'import python_pre_exec.myIGDIS_pre_exec; myIGDIS_pre_exec(input_file="./data/myIGDIs_Score_Export_SAMPLE_data_file.csv", output_file="./data/stacked_format_output.csv")'
```

Using an ID column from the assessment file and running earthmover on the pre processed file:

```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/stacked_format_output.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "StudentId"
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