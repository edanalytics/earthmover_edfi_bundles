* **Title**: ACCUPLACER Placement Tests - API 3.X
* **Description**: This template maps College Board Next-Generation ACCUPLACER files. It currently handles the placement tests only. It may be extended in the future to map ESL and Essay tests.
* **API version**: 5.2
* **Submitter name**: Samantha LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/accuplacer.csv</code></summary>
This template will only work with the ACCUPLACER placement test results file.
</details>

<details>
<summary><code>seeds/student_ids.csv</code></summary>

This is a [crosswalk file](https://en.wikipedia.org/wiki/Schema_crosswalk) for translating the student IDs in the assessment CSVs to student IDs in Ed-Fi (one may be a state ID and the other a district ID, for example). 

This file is **optional**. If one of the student ID column within the assessment file maps to Ed-Fi's `studentUniqueId`, you can omit the crosswalk file.

If you need to use a crosswalk, see the CLI parameters section below.

Required columns:
   - `student_id_from`
   - `student_id_to`
</details>

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- INPUT_FILE: The student assessment file to be mapped
- API_YEAR: The API year of the ODS for which we would send these records

### Optional
If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `student_id_from`, an ID included in the assessment file, and `student_id_to`, the `studentUniqueId` value in Ed-Fi

To query a student ID xwalk from a database, provide the following additional parameters:
- DATABASE_CONNECTION: [SQLAlchemy database URL](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- STUDENT_ID_QUERY: Crosswalk query with columns `student_id_from` and `student_id_to`. You may need to use `$$` in the place of single quotes to avoid issues with constructing the query string.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"STATE_FILE": "./state",
"INPUT_FILE": "path/to/BESS.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023" }'
```

Using a student ID crosswalk
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"STATE_FILE": "./state",
"INPUT_FILE": "path/to/BESS.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023"
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv" }'
```

Using a database connection:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"STATE_FILE": "./state",
"INPUT_FILE": "path/to/BESS.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023"
"DATABASE_CONNECTION": "database_connection_string"
"STUDENT_ID_QUERY": "select id_1 as student_id_from, id_2 as student_id_to from student_table" }'
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