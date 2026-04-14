## myIGDIs

* **Title**: myIGDIs Assessment Bundle - API 3.X
* **Description**: This template includes the myIGDIs assessments, designed to measure individual growth and development indicators across various domains.
* **API version**: 7.1
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC

To run this bundle, please add your own source file(s) and column(s):
<details>
This template works with vendor layout file structure. See the sample anonymized file.
</details>

Sample file: `data/sample_anonymized_file.csv`

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Default column is the `edFi_studentUniqueID` from the student ID crosswalk package.
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student ID columns in the assessment file (e.g., `Student Id`)

### Optional

- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as `ResultDatatypeTypeDescriptor`. The default value is: `uri://ed-fi.org`

### Examples

Running earthmover:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "data/sample_anonymized_file.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "Student Id"
}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with:
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "DATA_DIR": "./output/",
  "STATE_DIR": "./tmp/.lightbeam/",
  "EDFI_API_BASE_URL": "<yourURL>",
  "EDFI_API_CLIENT_ID": "<yourID>",
  "EDFI_API_CLIENT_SECRET": "<yourSecret>",
  "API_YEAR": "<yourAPIYear>"
}'
```
