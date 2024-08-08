This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Istation ISIP Assessment Results - API 3.X
* **Description**: This template is for the Istation Indicators of Student Progress Reading Difficulties Assessment and the Lectura Spanish Assessment.
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/isip_results.csv</code></summary>
This is the CSV download of Istation student result data. Files include an entire school year of data, with a set of columns for each month.

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
- INPUT_FILE: The assessment file to be mapped
- API_YEAR: The school year when the assessments were taken
- SUBJECT: `reading` or `spanish`. Istation's English reading and Spanish Lectura assessments are both supported. Defaults to `reading`.

### Optional
If student IDs must be mapped, there are two options. To use a CSV crosswalk, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `student_id_from`, an ID included in the assessment file, and `student_id_to`, the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_NAME: `student_id_to`

To query a student ID xwalk from a database, provide the following additional parameters:
- DATABASE_CONNECTION: [SQLAlchemy database URL](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- STUDENT_ID_QUERY: Crosswalk query with columns `student_id_from` and `student_id_to`. You may need to use `$$` in the place of single quotes to avoid issues with constructing the query string.
- STUDENT_ID_NAME: `student_id_to`
- ISTATION_ENDPOINT: `report` or `export` Istation provides all scores with its export endpoint, but in a significantly different format. Only specify `export` if your csv data is from the export endpoint or errors will occur. The default for Istation, and this bundle, is to assume the report format.  See documentation [HERE](https://help.istation.com/en_US/how-do-i-automate-data-exports) for details.

Istation performance levels can be reported on two different scales: tiers (1: >40th percentile, 2: 21-40th percentile, 3: <=20th percentile) or levels (5: >80th percentile, 4: 61-80th percentile, 3: 41-60th percentile, 2: 21-40th percentile, 1: <=20th percentile). Sometimes, it can be helpful to enforce a standard performance level if they vary across schools or districts. The included pre-populated seed tables `map_percentile_to_level` and `map_percentile_to_tier` can be used for this. They can also be edited to use a custom performance level.
- PERCENTILE_MAPPING: `level` or `tier`

### Examples
Using an ID column from the assessment file and optional percentile mapping:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"API_YEAR": "2023",
"SUBJECT": "reading",
"PERCENTILE_MAPPING": "level"}'
```

Using a student ID crosswalk:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"SUBJECT": "reading",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_NAME": "student_id_to"}'
```

Using a database connection:
```bash
earthmover run -c ./earthmover.yml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"SUBJECT": "reading",
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
