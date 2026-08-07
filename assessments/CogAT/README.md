This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Cognitive Abilities Test (CogAT) Assessment Results - API 3.X
* **Description**: This template maps data exported from the Riverside Insights DataManager Balanced Assessment data export
* **API version**: 5.3
* **Submitter name**: John C. Merfeld
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/cogat_export.txt</code> or <code>data/cogat_export.csv</code></summary>
This bundle works with CogAT 7 & 8, and takes any of the three files we see in practice.
There is a sample of each in `data/`:

| File | Looks like |
| --- | --- |
| `.txt` | fixed width, 5682 characters per row (layout in `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv`) |
| `.csv` | one column per subtest: `Standard Age Score (SAS) V`, `Standard Age Score (SAS) VQ` |
| `.csv` | one column per score: `Standard_Age_Score_SAS` = `107105117107114114112` |

The last one is the layout we publish as the loading spec; the middle one is what
DataManager exports. A fixed-width file must be named `.txt` — that is how the bundle tells
it apart from a CSV.

Capitalization, punctuation and extra spaces in CSV headers don't matter:
`Number Attempted (NA) V`, `Number_Attempted_NA_V` and `number attempted (na) v` all work.

</details>
<details>
<summary><code>seeds/student_ids.csv</code></summary>
This is a crosswalk file for translating the student IDs in the assessment CSVs to student IDs in Ed-Fi (one may be a state ID and the other a district ID, for example).

This file is **optional**. If one of the existing student IDs within the assessment
file maps to Ed-Fi's `studentUniqueId`, you can omit the crosswalk file and specify 
which column to use (e.g. `StudentID` or `Secondary_Student_ID`).

If neither of these match Ed-Fi's `studentUniqueId`, see the CLI parameters section below.

Required columns:
   - `student_id_from`
   - `student_id_to`
</details>

Once your input files are in place, run the following command. Earthmover reads both
formats directly, so no preprocessing step is required:
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

  - `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv` is the fixed-width layout. It matches
    `util/cogat_format.csv` except that each score field is split into one column per subtest
    (`Standard_Age_Score_SAS__verbal`, `..._composite_vq`, ...). That split matters: pandas
    trims spaces off both ends of a fixed-width field, and these values are right-aligned, so
    reading a score field whole would drop the first value's padding and shift the rest.
    Regenerate this file if the layout changes; don't hand-edit it.
  - `util/preprocessing.py` turns a fixed-width export into the one-column-per-score CSV.
    Earthmover reads the `.txt` directly now, so this is optional, but it still works and its
    output is still a valid input.
  - The seed file `seeds/performanceLevelDescriptors.csv` was generated using the script `util/generate_pl_descriptors.py`. This was done to ensure that all possible CogAT [Ability Profiles](https://riversideinsights.com/citc/profile-finder) would be represented. If, in a future edition of the test, the set of possible Ability Profiles changes, this script will need to be modified.