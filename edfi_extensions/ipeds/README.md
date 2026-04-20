* **Title**: Integrated Postsecondary Education Data System (IPEDS) Directory
* **Description**: This bundle maps an IPEDS Directory file to the Ed-Fi postSecondaryInstitutions endpoint. 
* **Submitter name**: Theo Kaufman
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<code>data/IPEDS Directory.csv</code>

Or use the sample file (`data/sample_ipeds_file.csv`).

## CLI Parameters

### Required
- OUTPUT_DIR: Where the output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The MVPA assessment results file to be mapped

### Examples

```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_ipeds_file.csv",
"OUTPUT_DIR": "output/"
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