## Iowa

* **Title:** Iowa Assessments
* **Description:** Achievement tests (part of “The Iowa Testing Programs.”)
* **API version:** 5.3
* **Submitter name:** Mariela Suárez
* **Submitter organization:** Crocus LLC.

To run this bundle, please add your own source file(s) and column(s):
<details>
This template will work with vendor layout file structure. See the sample anonymized file.
</details>

Sample file: `data/IOWA_deidentified_sample_file.csv`)

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Where to store the earthmover runs.csv file
- **INPUT_FILE**: The student assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Candidate columns are _Student_Id_ and _Secondary_Student_Id_ from the vendor layour file.
- **SCHOOL_YEAR**: The year of the assessment file (format as 'YYYY' e.g. '2024', etc).
- **DESCRIPTOR_NAMESPACE_OVERRIDE**: Default namespace prefix: `uri://ed-fi.org` (can be **overridden**)

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "data/IOWA_deidentified_sample_file.csv",
"STATE_FILE": "./tmp/runs.csv",
"OUTPUT_DIR": "output/",
"STUDENT_ID_NAME": "Student_Id",
"SCHOOL_YEAR": "2024"}'
```
# ,"DESCRIPTOR_NAMESPACE_OVERRIDE":"uri://ed.sc.gov"

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"STATE_DIR"="./tmp/.lightbeam/"
"EDFI_API_BASE_URL": "<yourURL>",
"EDFI_API_CLIENT_ID": "<yourID>",
"EDFI_API_CLIENT_SECRET": "<yourSecret>",
"SCHOOL_YEAR": "<yourAPIYear>" }'
```