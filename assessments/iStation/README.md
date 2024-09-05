This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Istation ISIP Assessment Results - API 3.X
* **Description**: This template is for the Istation Indicators of Student Progress Reading Difficulties Assessment and the Lectura Spanish Assessment.
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/isip_results.csv</code></summary>
This is the CSV download of Istation student result data retrieved from the API. You can use either the `report` or `export` endpoint.
</details>

Or use the sample file (data/sample_anonymized_file.csv).

## CLI Parameters
- OUTPUT_DIR: Where output files will be written
- STATE_FILE: Where to store the earthmover runs.csv file
- INPUT_FILE: The path to the assessment file to be mapped
- API_YEAR: The API year that the output of this template will be sent to
- STUDENT_ID_NAME: Which column to use as the Ed-Fi studentUniqueId. Default column is 'STUDENT_ID' from the Istation file.
- SUBJECT: `reading` or `spanish`, defaults to `reading`. Istation's English reading and Spanish Lectura assessments are both supported.
- ISTATION_ENDPOINT: `report` or `export`, defaults to `report`.
   - Istation provides all scores with its export endpoint, but in a significantly different format. Only specify `export` if your csv data is from the export endpoint or errors will occur. The default for Istation, and this bundle, is to assume the report format.  See documentation [HERE](https://help.istation.com/en_US/how-do-i-automate-data-exports) for details.
- PERCENTILE_MAPPING: `level` or `tier`, not used by default.
   - Istation performance levels can be reported on two different scales: tiers (1: >40th percentile, 2: 21-40th percentile, 3: <=20th percentile) or levels (5: >80th percentile, 4: 61-80th percentile, 3: 41-60th percentile, 2: 21-40th percentile, 1: <=20th percentile). Sometimes, it can be helpful to enforce a standard performance level if they vary across schools or districts. The included pre-populated seed tables `map_percentile_to_level` and `map_percentile_to_tier` can be used for this. They can also be edited to use a custom performance level.

### Examples
Using an ID column from the assessment file and optional percentile mapping:
```bash
earthmover run -c ./earthmover.yaml -p '{
"OUTPUT_DIR": "./output",
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "./data/sample_anonymized_file.csv",
"STUDENT_ID_NAME": "STUDENT_ID",
"API_YEAR": "2023",
"SUBJECT": "reading",
"ISTATION_ENDPOINT": "report",
"PERCENTILE_MAPPING": "tier" }'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "2023",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```
