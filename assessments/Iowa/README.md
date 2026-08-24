## Iowa

* **Title:** Iowa Assessments
* **Description:** Achievement tests (part of “The Iowa Testing Programs.”)
* **API version:** 5.3
* **Submitter name:** Mariela Suárez
* **Submitter organization:** Crocus LLC.

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/iowa_export.txt</code> or <code>data/iowa_export.csv</code></summary>
This bundle works with Iowa Assessments Form E, F & G and takes two files. There is a
sample of each in `data/`:

| File | Source |
| --- | --- |
| `.txt` | the canonical export from the vendor; layout in `fwf_to_csv_xwalks/iowa_fwf_xwalk.csv` |
| `.csv` | `input_student_id_no_match.csv` from a previous run, with the student IDs corrected |

</details>

### CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **STATE_FILE**: Where to store the earthmover runs.csv file
- **INPUT_FILE**: The student assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Candidate columns are `Student_ID` and `Secondary_Student_ID`.
- **DESCRIPTOR_NAMESPACE**: Default namespace prefix: `uri://ed-fi.org` (can be overridden)

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "data/sample_anonymized_file.txt",
"STATE_FILE": "./tmp/runs.csv",
"OUTPUT_DIR": "output/",
"API_YEAR": "2024",
"STUDENT_ID_NAME": "Student_ID"}'
```

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

### Maintenance notes

  - We read the FWF slightly differently from how Riverside defines its fields. Essentially, the vendor packs multiple scores into individual column; if you read these in as single fields, you have to then unpack the scores in the bundle. We instead define a slightly different colspec so that those columns are read in as unpacked scores. This is safer (it's hard to control how Pandas' `read_fwf` will handle blanks, etc) and makes it easier to accommodate both the FWF and the CSV input formats.