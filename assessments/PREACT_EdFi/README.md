This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: ACT (Ed-Fi Integration Source) - API 3.X
* **Description**: This template transforms data from ACT's Ed-Fi Integration, for two reasons. 1) to reshape the structure of objective assessments in accordance with Assessment governance decisions, and 2) to be able to utilize the student_id bundle package for aligning ACT source data to the correct student IDs.
* **API version**: 5.3
* **Submitter name**: Rob Little
* **Submitter organization**: Education Analytics

To run this bundle, you will need a database connection to a database where the ACT Ed-Fi data have been landed and unpacked into table form. 
<mark style="background-color: #FDFD96">Some aspects of this bundle are still under discussion - specifically the methods by which data should be sourced in the bundle.</mark>

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- ACT_SNOWFLAKE_CONNECTION: Connection string to snowflake database where the ACT source data have landed
- ACT_TENANT_CODE: tenant code to run, based on tenancy in the database where ACT source data have landed. Note, when using student_id_wrapper, this will be inferred from $SNOWFLAKE_TENANT_CODE by default.
- ACT_API_YEAR: YEAR to run, based on api_year in the database where ACT source data have landed. Note, when using student_id_wrapper, this will be inferred from $SNOWFLAKE_API_YEAR by default.

### Optional
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Default column is the 'edFi_studentUniqueID', with the assumption that the bundle is being wrapped by the [student_id_wrapper package](https://github.com/edanalytics/earthmover_edfi_bundles/tree/feature/act_edfi/packages/student_id_wrapper)
- POSSIBLE_STUDENT_ID_COLUMNS: List of student ID columns from the source ACT data to check against student ID source when using the [student_id_wrapper package](https://github.com/edanalytics/earthmover_edfi_bundles/tree/feature/act_edfi/packages/student_id_wrapper)
- ACT_SNOWFLAKE_EDU_STG_SCHEMA: EDU schema name within which the staging data (for student assessments) have landed
- ACT_SNOWFLAKE_EDU_BLD_SCHEMA: EDU schema name within which the build data (for student identification codes) have landed -- <mark style="background-color: #FDFD96">NOTE, this is subject to be removed after review by the team.</mark>

### Examples
Using the student ID wrapper package (preferred): (see that package's documentation for how to set up project composition to have it import the ACT_EdFi bundle).
```bash
earthmover run -c /path/to/earthmover_edfi_bundles/packages/student_id_wrapper/earthmover.yaml -p '{
"ASSESSMENT_BUNDLE": "ACT_EdFi",
"OUTPUT_DIR": "./output",
"EDFI_ROSTER_SOURCE_TYPE": "snowflake",
"ACT_SNOWFLAKE_CONNECTION": "snowflake://[USER]:[PASSWORD]@[ACCOUNT]?warehouse=[WAREHOUSE]",
"SNOWFLAKE_CONNECTION": "snowflake://[USER]:[PASSWORD]@[ACCOUNT]?warehouse=[WAREHOUSE]",
"SNOWFLAKE_TENANT_CODE": "[TENANT_CODE]",
"SNOWFLAKE_API_YEAR": "[API_YEAR]"
}'
```

Using the bundle directly (not recommended)
```bash
earthmover run -c earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STUDENT_ID_NAME": "registration_state_student_id", 
"ACT_SNOWFLAKE_CONNECTION": "snowflake://[USER]:[PASSWORD]@[ACCOUNT]?warehouse=[WAREHOUSE]",
"ACT_SNOWFLAKE_TENANT_CODE": "[TENANT_CODE]",
"ACT_SNOWFLAKE_API_YEAR": "[API_YEAR]"

```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c lightbeam.yaml -p '{
"DATA_DIR": "./output",
"API_YEAR": "[API_YEAR]",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
