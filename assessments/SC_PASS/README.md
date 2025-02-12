## SC PASS Assessments

* **Title:** DRC SC PASS Assessment Results - API 3.X
* **Description:** Data Recognition Corporation South Carolina College-and Career-Ready Assessment
* **API version:** 5.3
* **Submitter name:** Shailendra Singh
* **Contributor name:** Meeth Mehta
* **Submitter organization:** Double Line Inc.

To run this bundle, please add your own source file(s) and column(s):
<details>
This template will work with vendor layout file structure. See the sample anonymized file.
</details>

Or use the sample file (`data/sample_anonymized_file_SC_PASS.csv`).

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The student assessment file to be mapped
- STUDENT_ID_NAME: Which column to use as the Ed-Fi `studentUniqueId`. Default column is the 'StateID' from the SC PASS file.
- SCHOOL_YEAR: The year of the assessment file (format as 'YYYY' e.g. '2024', etc).

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c earthmover.yaml -p '{\"STATE_FILE\": \"./runs.csv\",\"INPUT_FILE\": \"data/sample_anonymized_file_SC_PASS.csv\",\"OUTPUT_DIR\": \"output/\",\"STUDENT_ID_NAME\":\"StateID\",\"SCHOOL_YEAR\": \"2017\",\"DESCRIPTOR_NAMESPACE_OVERRIDE\": \"uri://ed.sc.gov\"}' -f                             
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