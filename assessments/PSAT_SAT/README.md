This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: PSAT/SAT Results - API 3.X
* **Description**: This template includes the SAT, PSAT/NMSQT, and PSAT 8/9 assessments. 
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/Student_Data_File.csv</code></summary>
This bundle currently works with SAT, PSAT/NMSQT, and PSAT 8/9 files in the format provided by College Board. It is compatible with both the pencil and paper tests (~2016-2023) and newer digital tests (2024 and beyond).

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

## CLI Parameters

### Required
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- OUTPUT_DIR: Where output files will be written
- INPUT_FILE: The assessment file to be mapped
- TEST_TYPE: Identifies which assessment is being loaded from the current input file. Must be <code>SAT</code>, <code>PSAT/NMSQT</code>, or <code>PSAT 8/9</code>.
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (`secondary_school_student_id`, `district_student_id` or `state_student_id`), or a value mapped from a crosswalk (must be supplied)

### Optional
If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `from` and ID included in the assessment file and `to` the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_JOIN_COLUMN: Declare which column in the assessment file should be used for the crosswalk join (`secondary_school_student_id`, `district_student_id` or `state_student_id`).

When using an ID xwalk, set `STUDENT_ID_NAME` as `to`.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"TEST_TYPE": "SAT -or- PSAT/NMSQT -or- PSAT 8/9",
"STUDENT_ID_NAME": "secondary_school_student_id"}'
```

Using a student ID crosswalk
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"TEST_TYPE": "SAT -or- PSAT/NMSQT -or- PSAT 8/9",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_JOIN_COLUMN": "Student_StateID",
"STUDENT_ID_NAME": "to"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "2023",
"BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```