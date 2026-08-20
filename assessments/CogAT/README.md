This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Cognitive Abilities Test (CogAT) Assessment Results - API 3.X
* **Description**: This template maps data exported from the Riverside Insights DataManager Balanced Assessment data export
* **API version**: 5.3
* **Submitter name**: John C. Merfeld
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/cogat_export.txt</code> or <code>data/cogat_export.csv</code></summary>
This bundle works with CogAT 7 & 8 and takes two files. There is a sample of each in `data/`:

| File | Source |
| --- | --- |
| `.txt` | the canonical export from the vendor; layout in `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv` |
| `.csv` | `input_student_id_no_match.csv` from a previous run, with the student IDs corrected |


</details>

Once your input files are in place, run the following command:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file.txt",
"OUTPUT_DIR": "output/",
"API_YEAR" : "2023",
"STUDENT_ID_NAME" : "Student_ID"}'
```
The value for `STUDENT_ID_NAME` may vary

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"API_YEAR": "2023",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```

### Maintenance notes

  - We read the FWF slightly differently from how Riverside defines its fields. Essentially, the vendor packs multiple scores into individual column; if you read these in as single fields, you have to then unpack the scores in the bundle. We instead define a slightly different colspec so that those columns are read in as unpacked scores. This is safer (it's hard to control how Pandas' `read_fwf` will handle blanks, etc) and makes it easier to accommodate both the FWF and the CSV input formats.
  - The seed file `seeds/performanceLevelDescriptors.csv` was generated using the script `util/generate_pl_descriptors.py`. This was done to ensure that all possible CogAT [Ability Profiles](https://riversideinsights.com/citc/profile-finder) would be represented. If, in a future edition of the test, the set of possible Ability Profiles changes, this script will need to be modified.