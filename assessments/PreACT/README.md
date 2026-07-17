* **Title**: PreACT Assessment
* **Description**: PreACT is a multiple-choice assessment designed for 10th grade students that provides:
  - Early practice experience for the ACT test
  - Assessment of achievement in English, Mathematics, Reading, and Science
  - Insights to help students identify academic strengths and areas for improvement
  - Guidance for high school coursework planning and career exploration
* **API version**: 7.1
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC

This bundle works with PreACT files in CSV format or fixed-width `.txt` format as provided by the assessment vendor.

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Path to the state file for tracking runs
- **INPUT_FILE**: The assessment file to be mapped

### Optional
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Default is `edFi_studentUniqueID` (used with the student ID xwalk package). Set to a native column (e.g., `Stu_ID_Num`) when running the bundle directly.
- **POSSIBLE_STUDENT_ID_COLUMNS**: Native student ID columns in the assessment file. Default is `Stu_ID_Num`.
- **DESCRIPTOR_NAMESPACE**: Default namespace for descriptors such as ResultDatatypeTypeDescriptor. Default is `uri://ed-fi.org`.

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "./data/Records_anonymized.csv",
  "OUTPUT_DIR": "./output",
  "STATE_FILE": "./runs.csv",
  "STUDENT_ID_NAME": "Stu_ID_Num"
}'
```

Using a fixed-width file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "./data/Records_anonymized.txt",
  "OUTPUT_DIR": "./output",
  "STATE_FILE": "./runs.csv",
  "STUDENT_ID_NAME": "Stu_ID_Num"
}'
```

Once you have inspected the output JSONL for issues, check the settings in lightbeam.yaml and transmit them to your Ed-Fi API with:

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "OUTPUT_DIR": "./output",
  "STATE_FILE": "./runs.csv",
  "API_YEAR": "2021",
  "EDFI_API_BASE_URL": "yourURL",
  "EDFI_API_CLIENT_ID": "yourID",
  "EDFI_API_CLIENT_SECRET": "yourSecret"
}'
```
