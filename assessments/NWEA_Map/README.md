This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: NWEA MAP Growth Assessment Results - API 3.X
* **Description**: This template includes the NWEA MAP Growth Math and Reading Assessments. It covers vendor file exports AssessmentResults and ComboStudentAssessment, and handles format changes that have occurred over the last several years (as of 2023).
* **API version**: 5.2
* **Submitter name**: Erik Joranlien
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/AssessmentResults.csv</code></summary>
This bundle works with the standard NWEA Map exports AssessmentResults.csv or 
ComboStudentAssessment.csv.

It tries to retain compatibility across various versions of these file specifications
by looking for both the old and new names of changed columns.


</details>
<details>
<summary><code>seeds/student_ids.csv</code></summary>

This is a [crosswalk file](https://en.wikipedia.org/wiki/Schema_crosswalk) for translating the student IDs in the assessment CSVs to student IDs in Ed-Fi (one may be a state ID and the other a district ID, for example). 

This file is **optional**. If one of the existing student IDs within the assessment
file maps to Ed-Fi's `studentUniqueId`, you can omit the crosswalk file and specify 
which column to use (`StudentID` or `Student_StateID`).

If neither of these match Ed-Fi's `studentUniqueId`, see the CLI parameters section below.

Required columns:
   - `from`
   - `to`
</details>


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- INPUT_FILE: The assessment file to be mapped
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (`StudentID` or `Student_StateID`), or a value mapped from a crosswalk (must be supplied)

### Optional
If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `from` and ID included in the assessment file and `to` the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_JOIN_COLUMN: Declare which column in the assessment file should be used for the crosswalk join (`StudentID` or `Student_State_ID`)

When using an ID xwalk, set `STUDENT_ID_NAME` as `to`.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_NAME": "Student_StateID"}'
```

Using a student ID crosswalk
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_JOIN_COLUMN": "Student_StateID",
"STUDENT_ID_NAME": "to"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```

![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)


# Maintenance notes
There's an included file called `score_codegen.py` which uses the data in the seed tables to generate the long jinja snippets in the `jsont` files. 

Whenever the Map file changes format, we only need to add rows to `assessmentReportingMethodDescriptors.csv` (and change the `is_deprecated` field for any deprecated columns). 

Then, running `score_codegen.py` will generate a few blocks of code that can be pasted into the appropriate places in the `jsont` files. (This part of the process is manual).