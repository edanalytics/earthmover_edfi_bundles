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

| File | What it is |
| --- | --- |
| `.txt` | the vendor's fixed-width export — the canonical file. 5682 characters per row; layout in `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv` |
| `.csv` | `input_student_id_no_match.csv` from a previous run, with the student IDs corrected |

The CSV is **not** a vendor file. When a student can't be matched to Ed-Fi, the run writes
`input_student_id_no_match.csv`; users fix the IDs in it and submit it again. It matches no
DataManager export, and no DataManager CSV export is accepted — only this one.

A fixed-width file must be named `.txt`; that is how the bundle tells the two apart.

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

  - `fwf_to_csv_xwalks/cogat_fwf_xwalk.csv` gives each subtest its own column rather than
    reading a whole score field at once. Two reasons, both load-bearing. Reading a field whole
    would break the fixed-width read, because pandas trims spaces off both ends and the values
    are right-aligned, so the first one would lose its padding and shift the rest. And the
    no-match file is written by the `student_ids` package through a template that applies
    `|trim` to every value — a combined field would come back from a resubmission shifted by a
    character, silently, with no error. One value per column survives both. If you ever change
    this back to combined fields, the round-trip breaks.
  - The mode-of-administration flags are split the same way, into
    `Mode_of_Administration__00` through `__19`, and for the same reason: Riverside's layout
    says an omitted flag is `0` **or blank**, so reading the field whole would let a blank flag
    trim away and shift every flag after it. What each position means is written out in
    `earthmover.yaml`; note the column number is 0-based and so is one less than the position
    number in Riverside's document.
  - The seed file `seeds/performanceLevelDescriptors.csv` was generated using the script `util/generate_pl_descriptors.py`. This was done to ensure that all possible CogAT [Ability Profiles](https://riversideinsights.com/citc/profile-finder) would be represented. If, in a future edition of the test, the set of possible Ability Profiles changes, this script will need to be modified.