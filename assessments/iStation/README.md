This is an earthmover bundle created from the following Ed-Fi Data Import Tool mapping:
* **Title**: Istation ISIP Assessment Results - API 3.X
* **Description**: This template is for the Istation Indicators of Student Progress Reading Difficulties Assessment. 
* **API version**: 5.3
* **Submitter name**: Sam LeBlanc
* **Submitter organization**: Education Analytics

To run this bundle, please add your own source file(s) and column(s):
<details>
<summary><code>data/isip_results.csv</code></summary>
This is the CSV download of Istation student result data. Files include an entire school year of data, with a set of columns for each month.

</details>
<details>
<summary><code>seeds/map_student_id.csv</code></summary>

This is a [crosswalk file](https://en.wikipedia.org/wiki/Schema_crosswalk) for translating the student IDs in the assessment results CSV to student IDs in Ed-Fi (one may be a state ID and the other a local ID, for example). 

This file is **optional**. If the existing student IDs within the assessment file map to Ed-Fi's `studentUniqueId`, you can omit the crosswalk file.

If the student IDs in the file do not match Ed-Fi's `studentUniqueId`, see the CLI parameters section below.

Required columns:
   - `from`
   - `to`
</details>

## CLI Parameters

### Required
- OUTPUT_DIR: Where output files will be written
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives
- INPUT_FILE: The assessment file to be mapped

### Optional
If student IDs must be mapped, provide the following additional parameters:
- STUDENT_ID_XWALK: Path to a two-column CSV mapping `from` and ID included in the assessment file and `to` the `studentUniqueId` value in Ed-Fi
- STUDENT_ID_NAME: Defaults to the student ID column in the assessment file. When using an ID xwalk, set `STUDENT_ID_NAME` as `to`.

### Examples
Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
```

Using a student ID crosswalk
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/AssessmentResults.csv",
"OUTPUT_DIR": "./output",
"STUDENT_ID_XWALK": "path/to/student_id_xwalk.csv",
"STUDENT_ID_NAME": "to"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret" }'
```