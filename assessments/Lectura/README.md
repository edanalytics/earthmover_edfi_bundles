* **Title**: Lectura - API 3.X
* **Description**: This template maps Lectura assessment results files. 
* **API version**: 5.2
* **Submitter name**: Julianna Alvord and Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/StudentSummary.csv</code></summary>
</details>

<details>
<summary><code>seeds/student_ids.csv</code></summary>

This is a [crosswalk file](https://en.wikipedia.org/wiki/Schema_crosswalk) for translating the student IDs in the assessment CSVs to student IDs in Ed-Fi (one may be a state ID and the other a district ID, for example). 

This file is **optional**. If one of the existing student IDs within the assessment
file maps to Ed-Fi's `studentUniqueId`, you can omit the crosswalk file and specify 
which column to use.

If neither of these match Ed-Fi's `studentUniqueId`, see the CLI parameters section below.

Required columns:
   - `from`
   - `to`
</details>


## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- INPUT_FILE: The student assessment file to be mapped
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file, or a value mapped from a crosswalk (must be supplied)

### Optional
If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `student_id_from`, an ID included in the assessment file, and `student_id_to`, the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_FROM: Which column from the results file to use for mapping
- STUDENT_ID_NAME: `student_id_to`

To query a student ID xwalk from a database, provide the following additional parameters:
- DATABASE_CONNECTION: [SQLAlchemy database URL](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- STUDENT_ID_QUERY: Crosswalk query with columns `student_id_from` and `student_id_to`. You may need to use `$$` in the place of single quotes to avoid issues with constructing the query string.
- STUDENT_ID_FROM: Which column from the results file to use for mapping
- STUDENT_ID_NAME: `student_id_to`

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/StudentSummary.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_NAME": "Student Primary ID"}'
```

Using a student ID crosswalk
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE_OVERALL": "path/to/StudentSummary.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_FROM": "Student Primary ID",
"STUDENT_ID_NAME": "student_id_to"}'
```

Using a database connection:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/StudentSummary.csv",
"OUTPUT_DIR": "./output",
"DATABASE_CONNECTION": "database_connection_string"
"STUDENT_ID_QUERY": "select id_1 as student_id_from, id_2 as student_id_to from student_table",
"STUDENT_ID_FROM": "Student Primary ID",
"STUDENT_ID_NAME": "student_id_to"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```

![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)