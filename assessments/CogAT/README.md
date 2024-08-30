This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Cognitive Abilities Test (CogAT) Assessment Results - API 3.X
* **Description**: This template maps data exported from the Riverside Insights DataManager Balanced Assessment data export
* **API version**: 5.3
* **Submitter name**: John C. Merfeld
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s):
<details>
<summary><code>data/cogat_export.txt</code></summary>
This bundle currently works with CogAT 7 & 8. It assumes you are working with a fixed-width text file exported from Riverside Insights DataManager with a total row length of 5682 characters.

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

Once your input files are in place, you need to transform the fixed-width CogAT data into a CSV. This bundle includes a script and configuration file that accomplish this:

```bash
python3 util/preprocessing.py data/cogat_export.txt util/cogat_format.csv
```

This will output `cogat_export.csv`, which can be used as input to Earthmover. Run the following command:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file.csv",
"OUTPUT_DIR": "output/",
"SCHOOL_YEAR" : "2023",
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

  - The seed file `seeds/performanceLevelDescriptors.csv` was generated using the script `util/generate_pl_descriptors.py`. This was done to ensure that all possible CogAT [Ability Profiles](https://riversideinsights.com/citc/profile-finder) would be represented. If, in a future edition of the test, the set of possible Ability Profiles changes, this script will need to be modified.