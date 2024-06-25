This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Lexia Core5 - API 3.X
* **Description**: This template is for the Lexia Core5 assessment. It requires the Core5 YTD Export file and can include activity-level results from the Core5 Detailed Export if provided.
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>core5_ytd.csv</code></summary>

This is the CSV download of Core5 YTD Export. The Core5 YTD (Year to Date) Export provides a summary of a student’s work in Core5 for the current school year. There is one line per student who has used Core5 at least once in the current school year.

</details>
<details>
<summary><code>core5_detailed.csv</code></summary>

This **optional** file is the CSV download of Core5 Detailed Student Export. This file is optional. The Core5 Detailed Student Export provides a daily update of a student’s work in each activity. The CSV file contains a row for each Core5 program activity that each student has worked in (both current and historical).

</details>
<details>
<summary><code>seeds/map_student_id.csv</code></summary>

This is a [crosswalk file](https://en.wikipedia.org/wiki/Schema_crosswalk) for translating the student IDs in the assessment results CSV to student IDs in Ed-Fi (one may be a state ID and the other a local ID, for example). 

This file is **optional**. If the existing student IDs within the assessment file map to Ed-Fi's `studentUniqueId` or using a database connection, you can omit the crosswalk file.

If the student IDs in the file do not match Ed-Fi's `studentUniqueId`, see the CLI parameters section below.

Required columns:
   - `student_id_from`
   - `student_id_to`
</details>

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- YTD_FILE: Path to the Core5 YTD Export file
- API_YEAR: The API year that the output of this template will send to (e.g. the school year when the assessments were taken)
- STUDENT_ID_NAME: The snake-case name of the column that contains the students' Ed-Fi studentUniqueIds. The file may include `ref_id`, `state_id`, `sis_id`, and `student_number`.

### Optional

If you have a Core5 Detailed Student Export file to be mapped, add an additional parameter:
- DETAILED_FILE: Path to the Core5 Detailed Student Export file

If student IDs must be mapped, there are two options. To use a CSV crosswalk, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `student_id_from`, an ID included in the assessment file, and `student_id_to`, the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_NAME: `student_id_to`

To query a student ID xwalk from a database, provide the following additional parameters:
- DATABASE_CONNECTION: [SQLAlchemy database URL](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- STUDENT_ID_QUERY: Crosswalk query with columns `student_id_from` and `student_id_to`. You may need to use `$$` in the place of single quotes to avoid issues with constructing the query string.
- STUDENT_ID_NAME: `student_id_to`

### Examples
Using an ID column from the assessment file and optional detailed file:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"YTD_FILE": "path/to/Core5_YTD.csv",
"DETAILED_FILE": "path/to/Core5_Detailed.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023",
"STUDENT_ID_NAME": "snake_case_id_column_name"}'
```

Using a student ID crosswalk:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"YTD_FILE": "path/to/Core5_YTD.csv",
"DETAILED_FILE": "path/to/Core5_Detailed.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_NAME": "student_id_to"}'
```

Using a database connection:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"YTD_FILE": "path/to/Core5_YTD.csv",
"DETAILED_FILE": "path/to/Core5_Detailed.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023",
"DATABASE_CONNECTION": "database_connection_string"
"STUDENT_ID_QUERY": "select id_1 as student_id_from, id_2 as student_id_to from student_table",
"STUDENT_ID_NAME": "student_id_to"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "2023",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```