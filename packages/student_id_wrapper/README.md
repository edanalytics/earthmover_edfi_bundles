This earthmover project combines an assessment bundle with the student ID alignment bundle using [project composition](https://github.com/edanalytics/earthmover?tab=readme-ov-file#project-composition).

## Usage
The student ID bundle works by computing a join on every possible combination of the student ID columns in the assessment file and the student ID columns in Ed-Fi. It then chooses the combination with the highest match rate and uses a crosswalk to find the Ed-Fi student unique ID. 

The bundle produces a `student_id_match_rates.csv` which can be stored and reused on subsequent runs.

### Required parameters
* `ASSESSMENT_BUNDLE`: which assessment bundle to install and run. This must match the name of the `earthmover_edfi_bundles` directory for the assessment.
* `INPUT_FILE`: the (main) input file to process
* `OUTPUT_DIR`: the directory to which to write earthmover output files
* `EDFI_ROSTER_SOURCE_TYPE`: "file" or "snowflake"
    * If providing a file:
        * `EDFI_ROSTER_FILE`: a path to a JSONL file such as `./studentEducationOrganizationAssociations.jsonl`
    * If pulling from Snowflake (this is currently specific to EDU projects):
        * `SNOWFLAKE_EDU_STG_SCHEMA`: the EDU database and staging schema, such as `analytics.prod_stage`
        * `SNOWFLAKE_CONNECTION`: in the form of `snowflake://[username]:[password]@[account]?warehouse=[warehouse]`
        * `SNOWFLAKE_TENANT_CODE`: the `tenant_code` by which to filter
        * `SNOWFLAKE_API_YEAR`: the `api_year` by which to filter

To provide stored match rates:
* `MATCH_RATES_SOURCE_TYPE`: "file" or "snowflake"
    * If providing a file:
        * `MATCH_RATES_FILE`: a path to a CSV file such as `./student_id_match_rates.csv`
    * If pulling from Snowflake:
        * `MATCH_RATES_SNOWFLAKE_QUERY`: a query to pull match rates data stored in Snowflake
        * `SNOWFLAKE_CONNECTION`: in the form of `snowflake://[username]:[password]@[account]?warehouse=[warehouse]`

### Optional parameters
* `EDFI_STUDENT_ID_TYPES`: a comma-separated list of ID types from your Ed-Fi roster. Defaults to `Local,School,District,State`.
* `POSSIBLE_STUDENT_ID_COLUMNS`: a comma-separated list of columns from the `INPUT_FILE` that might contain student IDs. A default value is provided in each assessment bundle, but you may need to overwrite this if your file has a custom ID column.
* `REQUIRED_MATCH_RATE`: the minimum match rate required to proceed. If no pair of ID types with at least this match rate is found, earthmover will exit. Default value is 0.5.
* `EARTHMOVER_NODE_TO_XWALK`: the assessment bundle's node to which to apply the xwalked input file. Default is the standardized node name `$sources.input`.
* `ASSESSMENT_BUNDLE_BRANCH`: the name of the branch from which to install the bundle. **Note that this must be included when running `earthmover deps`, not `earthmover run`**. Defaults to `main`.

### Example of a first run (without stored match rates)
On the first run, calculate and output the best student ID match rates (they will materialize at {OUTPUT_DIR}/student_id_match_rates.csv). The rest of the run will be completed with the cross-walked IDs.

```
earthmover run -p '{
"ASSESSMENT_BUNDLE": "Bundle_Folder_Name",
"INPUT_FILE": "./FakeAssessmentFile.csv",
"OUTPUT_DIR": "./output/",
"EDFI_ROSTER_SOURCE_TYPE": "file",
"EDFI_ROSTER_FILE": "./studentEducationOrganizationAssociations.jsonl",
"POSSIBLE_STUDENT_ID_COLUMNS": "School_StateID,StudentID,Student_StateID",
"EDFI_STUDENT_ID_TYPES": "Local,District,State",
"REQUIRED_MATCH_RATE":0.5
}'
```

### Example of a second run (with stored match rates)
On subsequent runs, cross-walk student IDs using the (prevously-computed) match rate and produce Ed-Fi JSONL files.

```
earthmover run -p '{
"ASSESSMENT_BUNDLE": "Bundle_Folder_Name",
"INPUT_FILE": "./FakeAssessmentFile.csv",
"OUTPUT_DIR": "./output/",
"EDFI_ROSTER_SOURCE_TYPE": "file",
"EDFI_ROSTER_FILE": "./studentEducationOrganizationAssociations.jsonl",
"POSSIBLE_STUDENT_ID_COLUMNS": "School_StateID,StudentID,Student_StateID",
"EDFI_STUDENT_ID_TYPES": "Local,District,State",
"REQUIRED_MATCH_RATE":0.5,
"MATCH_RATES_SOURCE_TYPE": "file",
"MATCH_RATES_FILE": "./output/student_id_match_rates.csv"
}'
```

## Implementation notes
The [project composition](https://github.com/edanalytics/earthmover?tab=readme-ov-file#project-composition) feature of earthmover requires packages to be installed before the `earthmover run`. The `ASSESSMENT_BUNDLE` parameter must be included when running `earthmover deps`. The `ASSESSMENT_BUNDLE_BRANCH` parameter is optional. Example:

```
earthmover deps -p '{
"ASSESSMENT_BUNDLE": "Bundle_Folder_Name",
"ASSESSMENT_BUNDLE_BRANCH": "feature/my_new_branch",
}'
```