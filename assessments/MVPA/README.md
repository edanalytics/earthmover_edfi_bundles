* **Title**: MVPA
* **Description**: This is a template bundle that will map MVPA assessments. 
* **Submitter name**: Theo Kaufman
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<code>data/MVPA.csv</code>

Or use the sample file (`data/sample_anonymized_file.csv`).

## CLI Parameters

### Required
- OUTPUT_DIR: Where the output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The MVPA assessment results file to be mapped
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Default column is `StudentID`.

### Examples

Using the `StudentID` column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file.csv",
"OUTPUT_DIR": "output/" ,
"STUDENT_ID_NAME": "StudentID",
"EDFI_DS_VERSION": "4"
}'
```

Once you have inspected the output JSONL for issues, check the settings in lightbeam.yaml and transmit them to your Ed-Fi API with:
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```

## DAG Graph
![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)