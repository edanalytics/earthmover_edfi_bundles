# PSAT/SAT Assessment Bundle

Earthmover bundle for College Board PSAT and SAT assessments.

## Assessment Types Supported

This bundle supports the following College Board assessments:
- **PSAT 8/9**: For students in grades 8-9
- **PSAT 10**: For students in grade 10
- **PSAT/NMSQT**: For students in grades 11-12 (National Merit Scholarship Qualifying Test)
- **SAT**: For students in grades 11-12 and postsecondary

## Data Requirements

### Required Columns

The bundle automatically detects the assessment type based on the columns present in your data file.

**For PSAT data:**
- `STATE_STUDENT_ID` or `DISTRICT_STUDENT_ID` or `SECONDARY_ID`
- `LATEST_PSAT_DATE` - Administration date
- `LATEST_PSAT_TOTAL` - Total score
- `LATEST_PSAT_EBRW` - Evidence-Based Reading and Writing score
- `LATEST_PSAT_MATH_SECTION` - Mathematics section score

**For SAT data:**
- `STATE_STUDENT_ID` or `DISTRICT_STUDENT_ID` or `SECONDARY_ID`
- `LATEST_SAT_DATE` - Administration date
- `LATEST_SAT_TOTAL` - Total score
- `LATEST_SAT_EBRW` - Evidence-Based Reading and Writing score
- `LATEST_SAT_MATH_SECTION` - Mathematics section score

### Optional Columns

**PSAT subscale scores:**
- `LATEST_PSAT_READING` - Reading test score
- `LATEST_PSAT_WRIT_LANG` - Writing and Language test score
- `LATEST_PSAT_MATH_TEST` - Math test score
- `LATEST_PSAT_ADV_MATH` - Advanced Math subscale
- `LATEST_PSAT_HEART_ALGEBRA` - Heart of Algebra subscale
- `LATEST_PSAT_PROBSLV_DATA` - Problem Solving and Data Analysis subscale
- `LATEST_PSAT_EXPR_IDEAS` - Expression of Ideas subscale
- `LATEST_PSAT_ENG_CONVENT` - Standard English Conventions subscale
- `LATEST_PSAT_WORDS_CONTEXT` - Words in Context subscale
- `LATEST_PSAT_COMM_EVIDENCE` - Command of Evidence subscale

**SAT subscale scores:**
- `LATEST_SAT_READING` - Reading test score
- `LATEST_SAT_WRIT_LANG` - Writing and Language test score
- `LATEST_SAT_MATH_TEST` - Math test score

**Percentiles and benchmarks:**
- `PERCENTILE_COUNTRY_TOTAL` - National total percentile
- `PERCENTILE_COUNTRY_RW` - National reading/writing percentile
- `PERCENTILE_COUNTRY_MATH` - National math percentile
- `SELECTION_INDEX` - National Merit Selection Index (PSAT/NMSQT only)
- `EBRW_CCR_BENCHMARK` - Met EBRW College and Career Readiness Benchmark (Y/N)
- `MATH_CCR_BENCHMARK` - Met Math College and Career Readiness Benchmark (Y/N)

**Grade level:**
- `LATEST_PSAT_GRADE` or `LATEST_SAT_GRADE` - Grade level when assessed

## Sample Data Files

Reference files are located on the N drive at:
```
N:\south_carolina\sc_2024\assessment_loading\format_conversion\20_final_output\
```

Subdirectories:
- `psat89/most_recent/` - PSAT 8/9 files
- `psat10/most_recent/` - PSAT 10 files
- `psat/most_recent/` - PSAT/NMSQT files
- `sat_enrich/most_recent/` - SAT files

Anonymized sample files are available in the `data/` directory:
- `sample_psat89_anonymized.csv`
- `sample_psat10_anonymized.csv`
- `sample_psat_anonymized.csv`
- `sample_sat_anonymized.csv`

## Usage

### Run Earthmover

```bash
earthmover run -c ./earthmover.yaml -p '{
  "STATE_FILE": "./runs.csv",
  "INPUT_FILE": "path/to/your/psat_or_sat_file.csv",
  "OUTPUT_DIR": "output/",
  "STUDENT_ID_NAME": "STATE_STUDENT_ID",
  "API_YEAR": "2024"
}'
```

### Parameters

- `STATE_FILE`: Path to earthmover runs log file (e.g., `./runs.csv`)
- `INPUT_FILE`: Path to your PSAT or SAT data file
- `OUTPUT_DIR`: Directory for output JSONL files
- `STUDENT_ID_NAME`: The student ID column to use (default: `edFi_studentUniqueID` from student ID xwalking)
- `API_YEAR`: School year for the assessment (e.g., `2024`)
- `POSSIBLE_STUDENT_ID_COLUMNS`: Comma-separated list of possible student ID columns for xwalking (default: `STATE_STUDENT_ID,DISTRICT_STUDENT_ID,SECONDARY_ID`)

### Run Lightbeam

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "DATA_DIR": "./output/",
  "EDFI_API_BASE_URL": "https://your-edfi-api.example.com",
  "EDFI_API_CLIENT_ID": "your_client_id",
  "EDFI_API_CLIENT_SECRET": "your_client_secret",
  "API_YEAR": "2024"
}'
```

## Output Files

The bundle generates the following Ed-Fi JSONL files:

- `assessmentReportingMethodDescriptors.jsonl` - Descriptor values for reporting methods
- `performanceLevelDescriptors.jsonl` - Descriptor values for performance levels
- `assessments.jsonl` - Assessment definitions
- `objectiveAssessments.jsonl` - Objective assessment (section) definitions
- `studentAssessments.jsonl` - Student assessment results

## Assessment Identification

The bundle automatically identifies the assessment type:

1. If the file contains `LATEST_SAT_DATE`, it's identified as **SAT**
2. If the file contains `LATEST_PSAT_GRADE`:
   - Grade 8 or 9 → **PSAT 8/9**
   - Grade 10 → **PSAT 10**
   - Other grades → **PSAT/NMSQT**
3. Default → **PSAT/NMSQT**

## Notes

- **Student ID Xwalking**: This bundle includes student ID crosswalking logic. If you have an Ed-Fi roster file, set the appropriate parameters to match student IDs automatically.
- **Performance Levels**: College and Career Readiness Benchmarks are included if `EBRW_CCR_BENCHMARK` or `MATH_CCR_BENCHMARK` columns are present and contain Y/N values.
- **Multiple Administrations**: The College Board data files may include multiple test administrations (ADMIN2, ADMIN3, etc.). This bundle processes only the latest administration. Additional development would be needed to handle multiple administrations.

## Ed-Fi Compatibility

- **Ed-Fi Data Standard**: 3.x, 4.x, 5.x
- **earthmover version**: >=0.2.0

## Resources

- [College Board Official Website](https://www.collegeboard.org/)
- [PSAT/NMSQT Information](https://collegereadiness.collegeboard.org/psat-nmsqt-psat-10)
- [SAT Information](https://collegereadiness.collegeboard.org/sat)
- [Ed-Fi Assessment Domain](https://edfi.atlassian.net/wiki/spaces/EFDS/pages/20874650/Assessment+Domain)
