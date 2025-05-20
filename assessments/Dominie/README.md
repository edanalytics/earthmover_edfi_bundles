* **Title**:  Dominie - API 3.X
* **Description**: The Dominie Reading and Writing Assessment Portfolio is a comprehensive literacy assessment tool designed for students from kindergarten through third grade. It serves both formative and summative assessment purposes, allowing educators to monitor and support early literacy development effectively.
* **API version**: 5.3
* **Submitter name**: Mariela Suárez
* **Submitter organization**: Crocus LLC
  
To run this bundle, please add your own source file or use the sample file (<code>data/Dominie_anonymized_sample_file.csv</code>).

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written.
- **INPUT_FILE**: The assessment file to be mapped.
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be these columns in the assessment file: `suns`, `student_number` when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID`. 


### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor. The default value is: uri://ed-fi.org.
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file (e.g., `suns`, `student_number`). 


### Examples

Run the following command:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/Dominie_sample_anonymized_file.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "suns",
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

