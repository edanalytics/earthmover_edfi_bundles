* **Title**: Smarter Balanced Assessment Consortium (SBAC) Summative Assessments
* **Description**: Maps the SBAC summative assessments in English Language Arts/Literacy and Mathematics. SBAC is a multi-state consortium, so this bundle is deliberately written to avoid being specific to any one member state.
* **Submitter name**: Angelica Lastra
* **Submitter organization**: Education Analytics

> **Status: under development.**

## Model

Smarter Balanced is a consortium summative assessment given in **English Language Arts/Literacy** and **Mathematics**. Every member state administers it in grades 3 through 8 plus one high school grade, and **that high school grade is a per-state choice**: Washington tests grade 10, California tests grade 11.

### Assessments

Split into two by academic subject:

- **ELA/Literacy**
- **Mathematics**

For each subject the following are reported:

- **Scale score**, on a continuous scale of roughly 2000 to 3000 that shifts upward with grade level.
- **Standard error of measurement (SEM).**
- **Error band minimum and maximum**, provided as explicit columns rather than computed from the SEM.
- **Achievement level**, always 1 through 4.

### Objective assessments

Objective Assessments are defined by the consortium, so this structure is the same in every member state. ELA has four objective assessments, Mathematics has three.

| | ELA | Mathematics |
| --- | --- | --- |
| OA 1 | Reading | Concepts and Procedures |
| OA 2 | Writing | Problem Solving and Modeling/Data Analysis |
| OA 3 | Listening | Communicating Reasoning |
| OA 4 | Research/Inquiry | N/A |

States may instead (or additionally) report **composite objective assessments**, a more robust rollup of the same content:

| | ELA | Mathematics |
| --- | --- | --- |
| OA 1 | Reading and Listening | Concepts and Procedures |
| OA 2 | Writing and Research | Mathematical Practices |

For ELA, Reading and Listening collapse into one composite and Writing and Research collapse into the other. 
For Mathematics, Concepts and Procedures carries over and the remaining three objective assessments collapse into Mathematical Practices.

A single student record can carry objective assessment results at two different grains, and states may differ in which grain they publish.

## CLI Parameters

- `OUTPUT_DIR`: Where output files will be written.
- `STATE_FILE`: Where to store the earthmover runs.csv file.
- `INPUT_FILE`: The student assessment file to be mapped.
- `API_YEAR`: The API year of the ODS these records will be sent to.
- `STUDENT_ID_NAME`: Which column to use as the Ed-Fi `studentUniqueId`.

### Examples

[TBD]

## Lightbeam

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```
