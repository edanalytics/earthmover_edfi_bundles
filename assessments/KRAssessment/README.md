* **Title**: Kindergarten Readiness Assessment (KRA) - API 3.X
* **Description**: This template includes the KRA assessments, designed to measure individual readiness across various domains.
* **API version**: 5.3
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file
<details>
<summary><code>data/KRA_Data_File.csv</code></summary>

This bundle works with KRA files in the format provided by the assessment vendor. For details about the mapping look at the [mapping document](./mapping.md) found here.

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `StudentID`, `StateStudentID`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `StudentID`, `StateStudentID` ) . 

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/KRA_Data_File.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "StudentID"
}'
```