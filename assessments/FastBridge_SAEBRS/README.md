## FastBridge SAEBRS

* **Title:** FastBridge SAEBRS / mySAEBRS
* **Description:** Maps FastBridge SAEBRS (teacher) and mySAEBRS (student) screening results from the wide season-based vendor export into Ed-Fi Assessments, ObjectiveAssessments, and StudentAssessments. Social, Academic, and Emotional subscales are modeled as objective assessments; overall risk, percentiles, item totals, and growth metrics are mapped on the student assessment.
* **API version:** 5.3
* **Submitter name:** Education Analytics
* **Submitter organization:** Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
This template works with the vendor FastBridge SAEBRS results layout. See the sample anonymized file for reference.

The input CSV should contain:
- Student demographic columns (Local ID, State ID, First Name, Last Name, Grade, etc.)
- Season-specific Student and Teacher SAEBRS columns (Total Items, Items Correct, Social/Academic/Emotional subscales, percentiles, risk level, final date)
- Growth columns between seasons (duplicated once for Student and once for Teacher within each season block)
</details>

Sample file: `data/sample_anonymized_file.csv`

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Where to store the earthmover runs.csv file
- **INPUT_FILE**: The student assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Default is the column added by the student ID xwalk package.
- **API_YEAR**: The year of the assessment file (format as 'YYYY' e.g. '2024', etc).

### Examples

Running earthmover:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "data/sample_anonymized_file.csv",
"OUTPUT_DIR": "output/",
"STATE_FILE": "./runs.csv",
"STUDENT_ID_NAME": "Local ID",
"API_YEAR": "2024"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"STATE_DIR": "./tmp/.lightbeam/",
"EDFI_API_BASE_URL": "<yourURL>",
"EDFI_API_CLIENT_ID": "<yourID>",
"EDFI_API_CLIENT_SECRET": "<yourSecret>",
"API_YEAR": "<yourAPIYear>"}'
```
