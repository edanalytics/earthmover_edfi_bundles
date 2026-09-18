## FastBridge Progress Monitoring

* **Title:** FastBridge Progress Monitoring Assessment Results
* **Description:** This template maps FastBridge Progress Monitoring (PM) exports into Ed-Fi Assessments and StudentAssessments. It covers progress monitoring measures across CBMMath (CAP and Fluency), CBM-R, COMP Efficiency, Early Reading English (ERAS), and Early Math (EMATH). The vendor file is already in long format (one score metric per row); earthmover pivots score metrics onto each student assessment administration, takes the max when duplicate metric rows exist, and builds assessment identifiers with a `_PM` suffix.
* **Submitter name:** Ryan Aguilar
* **Submitter organization:** Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/FastBridge_ProgressMonitoring.csv</code></summary>
This bundle works with FastBridge Progress Monitoring files in the long-format layout provided by the vendor (columns such as `Assessment`, `AssessmentDate`, `Grade`, `ScoreMetric`, and `Score`). See the sample anonymized file for expected column names.
</details>

Sample file: `data/sample_anonymized_file_early_reading_eng.csv`

### Supported assessments

- **CBMMath CAP** and **CBMMath Fluency** measures (including grade-level GOMs and fluency variants)
- **CBM-R**
- **COMP_EFFICIENCY**
- **Early Reading English (ERAS)** measures (`ERAS-drw`, `ERAS-ln`, `ERAS-ls`, `ERAS-nw`, `ERAS-os`, `ERAS-sw`, `ERAS-wb`, `ERAS-ws`)
- **Early Math (EMATH)** measures (`EMATH-decomp-I`, `EMATH-ident-I`, `EMATH-ident-KG`, `EMATH-matchq`, `EMATH-numseq-KG`, `EMATHplacev`)

### CLI Parameters

### Required

- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The Progress Monitoring assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `Student Id`, `Student State Id`) when the bundle is run directly. Otherwise, leave the default value `edFi_studentUniqueID`
- **POSSIBLE_STUDENT_ID_COLUMNS**: All possible native student ID columns in the assessment file (defaults: `Local ID,State ID`)

### Optional

- **STATE_FILE**: Where to store the earthmover `runs.csv` file
- **DESCRIPTOR_NAMESPACE**: Default namespace for descriptors such as `ResultDatatypeTypeDescriptor`. Default: `uri://ed-fi.org`
- **API_YEAR**: School year sent on student assessments (format `YYYY`, e.g. `2025`). Default: `2025`

## Running this bundle without Student ID Xwalking

To run this bundle without implementing the student ID xwalking packages:

```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "data/sample_anonymized_file_early_reading_eng.csv",
  "OUTPUT_DIR": "./output",
  "STATE_FILE": "./runs.csv",
  "STUDENT_ID_NAME": "Student Id",
  "API_YEAR": "2025"
}'
```

## Lightbeam

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
