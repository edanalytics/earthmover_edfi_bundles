This package aligns student IDs from source data with known IDs from EdFi.

## Usage

Assuming you have an earthmover project which uses an assessment bundle, such as
```yaml
packages:
  NWEA_Map:
    git: https://github.com/edanalytics/earthmover_edfi_bundles.git
    subdirectory: assessments/NWEA_Map
```
and the required configuration for the assessment bundle (`INPUT_FILE`, etc.), you can use these student ID crosswalking packages as follows:

1. add the `student_ids` package to your earthmover project:
    ```yaml
    packages:
      compute_match_rates:
        git: https://github.com/edanalytics/earthmover_edfi_bundles.git
        branch: student_id_alignment_unified
        subdirectory: packages/student_ids
    ```
1. specify wether your source of student IDs known to EdFi is a query against an [Enable Data Union (EDU)](https://enabledataunion.org/) Ed-Fi data warehouse or a JSONL file (which you might pull from an Ed-Fi ODS using a tool like [`lighbeam`](https://github.com/edanalytics/lightbeam) with a command like `lightbeam fetch -s studentEducationOrganizationAssociations -k studentIdentificationCodes,educationOrganizationReference,studentReference`
1. specify the list of column names from your INPUT_FILE which *may contain* student IDs via an environment variable called `POSSIBLE_STUDENT_ID_COLUMNS` (for example `POSSIBLE_STUDENT_ID_COLUMNS=School_StateID,StudentID,Student_StateID`)
1. specify the possible values of `studentIdentificationCodes.assigningOrganizationIdentificationCode` in EdFi via an environment variable called `EDFI_STUDENT_ID_TYPES` (for example `EDFI_STUDENT_ID_TYPES=Local,District,State`)
1. specify the assessment file source node with student IDs via an environment variable called `EARTHMOVER_NODE_TO_XWALK` (for example `EARTHMOVER_NODE_TO_XWALK=\$sources.nwea_map_input`)
1. specify the minimum required match rate `REQUIRED_MATCH_RATE` (for example `REQUIRED_ID_MATCH_RATE=0.5`) to make the process exit if no pair of IDs with sufficient match rate is found
1. Override the source of the main/first input node of the assessment bundle with your xwalked input:
```yaml
transformations:
  nwea_map_student_assessment:
    source: $transformations.input_xwalked
```


Example of a first run (no stored match rates):
```bash
earthmover run -p '{
"POSSIBLE_STUDENT_ID_COLUMNS":"School_StateID,StudentID,Student_StateID",
"EDFI_ROSTER_SOURCE_TYPE": "file",
"EDFI_ROSTER_FILE": "./studentEducationOrganizationAssociations.jsonl",
"EDFI_STUDENT_ID_TYPES":"Local,District,State",
"EARTHMOVER_NODE_TO_XWALK":"$sources.nwea_map_input",
"REQUIRED_ID_MATCH_RATE": 0.5,
"BUNDLE_DIR":"./",
"INPUT_FILE":"path/to/file.csv",
"OUTPUT_DIR": "./"}'
```


Example of a second run (with stored match rates):
```bash
earthmover run -p '{
"EARTHMOVER_NODE_TO_XWALK":"$sources.nwea_map_input",
"EDFI_STUDENT_ID_TYPES":"Local,District,State",
"REQUIRED_ID_MATCH_RATE": 0.5,
"BUNDLE_DIR":"./",
"INPUT_FILE":"path/to/file2.csv",
"STUDENT_ID_NAME": "edFi_studentUniqueID",
"OUTPUT_DIR": "./output/"}'
```


## Design

This package works by
* computing a join on every possible combination of `POSSIBLE_STUDENT_ID_COLUMNS` and `EDFI_STUDENT_ID_TYPES`
* choosing the combination with the best match rate
* producing `best_id_match_rates.csv` which can be stored and reused on subsequent runs via `MATCH_RATES_SOURCE_TYPE="file"` and `MATCH_RATES_FILE` (to save recomputing all the joins)
* also producing `input_no_student_id_match.csv`, which is the `EARTHMOVER_NODE_TO_XWALK`'s row that *did not match* any Ed-Fi student ID
