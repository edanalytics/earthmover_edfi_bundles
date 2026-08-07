This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Cognitive Abilities Test (CogAT) Assessment Results - API 3.X
* **Description**: This template maps data exported from the Riverside Insights DataManager Balanced Assessment data export
* **API version**: 5.3
* **Submitter name**: John C. Merfeld
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/cogat_export.txt</code> or <code>data/cogat_export.csv</code></summary>
This bundle works with CogAT 7 & 8, and takes any of the three files we see in practice. At this time it's not clear what we should consider the canonical export from the Riverside Insights DataManager, but that is a problem for another day.
There is a sample of each in `data/`:

| File | Looks like |
| --- | --- |
| `.txt` | fixed width, 5682 characters per row (layout in `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv`) |
| `.csv` | one column per subtest: `Standard Age Score (SAS) V`, `Standard Age Score (SAS) VQ` |
| `.csv` | one column per score: `Standard_Age_Score_SAS` = `107105117107114114112` |

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

  - We are trying to accommodate two different formats of CSV that we have seen. One matches the FWF and has individual columns containing strings of different scores packed together. We also see CSVs where the score columns are broken out. In order to accept all of this in a single bundle, the "fixed-width-like" CSV still needs to adhere to the column widths in the colspecs. We haven't yet encountered any that don't, but this is a risk, and a place to start debugging if your CSV input is producing gibberish outputs.
  - The seed file `seeds/performanceLevelDescriptors.csv` was generated using the script `util/generate_pl_descriptors.py`. This was done to ensure that all possible CogAT [Ability Profiles](https://riversideinsights.com/citc/profile-finder) would be represented. If, in a future edition of the test, the set of possible Ability Profiles changes, this script will need to be modified.