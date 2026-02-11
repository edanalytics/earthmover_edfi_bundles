* **Title**: PreACT Assessment - API 7.1
* **Description**: PreACT is a multiple-choice assessment designed for 10th grade students that provides:
  - Early practice experience for the ACT test
  - Assessment of achievement in English, Mathematics, Reading, and Science
  - Insights to help students identify academic strengths and areas for improvement
  - Guidance for high school coursework planning and career exploration
* **API version**: 7.1
* **Submitter name**: Bruk Woldearegay
* **Submitter organization**: CrocusLLC
To run this bundle, please add your own source file<code>data/PreACT_Data_File.csv</code>

This bundle works with PreACT files in the format provided by the assessment vendor (namely fixed-width .txt files). 

## CLI Parameters

### Required
- **OUTPUT_DIR**: Where output files will be written
- **INPUT_FILE**: The assessment file to be mapped
- **STUDENT_ID_NAME**: Which column to use as the Ed-Fi `studentUniqueId`. Can be one of the native columns in the assessment file (e.g., `Stu_ID_Num`) when the bundle is run directly. Otherwise leave the default value `edFi_studentUniqueID` 
- **POSSIBLE_STUDENT_ID_COLUMNS**: This should contain all the possible native student id columns in the assessment file( e.g., `Stu_ID_Num`) . 
### Optional
- **DESCRIPTOR_NAMESPACE**: This should be the default namespace for descriptors such as ResultDatatypeTypeDescriptor . The default value is : uri://ed-fi.org

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c ./earthmover.yaml -p '{
  "INPUT_FILE": "path/to/PreACT_Data_File.csv",
  "OUTPUT_DIR": "./output",
  "STUDENT_ID_NAME": "Stu_ID_Num"
}'
```

Once you have inspected the output JSONL for issues, check the settings in lightbeam.yaml and transmit them to your Ed-Fi API with:

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "DATA_DIR": "./output/",
  "API_YEAR": "yourAPIYear",
  "BASE_URL": "yourURL",
  "EDFI_API_CLIENT_ID": "yourID",
  "EDFI_API_CLIENT_SECRET": "yourSecret"
}'
```