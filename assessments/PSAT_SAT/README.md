# PSAT/SAT Assessment Bundle

Converts College Board SAT Suite of Assessments data to Ed-Fi format.

## Supported Assessments

This bundle supports all assessments in the SAT Suite:

- **PSAT 8/9** - Grades 8-9, scores 240-1440
- **PSAT 10** - Grade 10, scores 320-1520
- **PSAT/NMSQT** - Grades 10-11, scores 320-1520 (National Merit Scholarship Qualifying Test)
- **SAT (current)** - Grades 11-12, scores 400-1600 (March 2016+ format with 2 sections: EBRW and Math)
- **SAT (Pre-2016)** - Grades 11-12, scores 600-2400 (Pre-March 2016 format with 3 sections: Critical Reading, Math, Writing)

## Data Structure

The bundle automatically detects test type and format based on:
- File path patterns (`psat89`, `psat10`, `psat`, `sat_enrich`)
- Column name patterns (`LATEST_PSAT_*` vs `LATEST_SAT_*`)
- For SAT: presence of `LATEST_SAT_EBRW` (new format) vs `LATEST_SAT_CRITICAL_READING` (old format)

## Grade Level Calculation

Grade level is calculated dynamically from cohort year and test date:
```
school_year = test_year (if fall/winter) or test_year - 1 (if spring/summer)
grade = 12 - (cohort_year - school_year)
```

**Note:** Students can take any test at any grade level, so grade is always calculated rather than assumed from test type.

## Usage

### Basic Example (PSAT)

```bash
earthmover run -c earthmover.yaml -p '{
  "INPUT_FILE": "data/sample_psat.csv",
  "API_YEAR": 2024
}'
```

### Example with Test Type Specified

```bash
earthmover run -c earthmover.yaml -p '{
  "INPUT_FILE": "path/to/sat_data.csv",
  "API_YEAR": 2024,
  "TEST_TYPE": "sat"
}'
```

### Required Parameters

- `INPUT_FILE`: Path to CSV file with PSAT or SAT data
- `API_YEAR`: School year for the data (e.g., 2024 for 2023-24 school year)

### Optional Parameters

- `OUTPUT_DIR`: Output directory (default: `./output/`)
- `STATE_FILE`: Earthmover state file path (default: `./earthmover_state.csv`)
- `STUDENT_ID_NAME`: Column name for student ID (default: `STATE_STUDENT_ID`)
- `TEST_TYPE`: Force test type detection - `psat89`, `psat10`, `psat`, `sat`, or `auto` (default: `auto`)
- `ASSESSMENT_NAMESPACE`: Assessment namespace URI (default: `uri://collegeboard.org/sat-suite/`)
- `DESCRIPTOR_NAMESPACE`: Ed-Fi descriptor namespace URI (default: `uri://ed-fi.org/`)

## Required Columns

### All Tests
- `COHORT_YEAR`: Expected graduation year (for grade calculation)
- `STATE_STUDENT_ID`: Student identifier (or column specified by `STUDENT_ID_NAME`)

### PSAT Tests
- `LATEST_PSAT_DATE`: Test date (ISO format: YYYY-MM-DD)
- `LATEST_PSAT_TOTAL`: Total score

### SAT Tests
- `LATEST_SAT_DATE`: Test date (ISO format: YYYY-MM-DD)
- `LATEST_SAT_TOTAL`: Total score

## Optional Columns

### New Format (PSAT and SAT 2016+)
- `LATEST_PSAT_EBRW` or `LATEST_SAT_EBRW`: Evidence-Based Reading and Writing section score
- `LATEST_PSAT_MATH_SECTION` or `LATEST_SAT_MATH_SECTION`: Math section score

### Old SAT Format (Pre-2016)
- `LATEST_SAT_CRITICAL_READING`: Critical Reading section score
- `LATEST_SAT_MATH`: Mathematics section score
- `LATEST_SAT_WRITING`: Writing section score

### Performance Levels
- `EBRW_CCR_BENCHMARK`: College and Career Readiness benchmark for EBRW (Y/N)
- `MATH_CCR_BENCHMARK`: College and Career Readiness benchmark for Math (Y/N)

## Output

The bundle generates three JSONL files:

- `assessments.jsonl`: Assessment entity definitions for each test type
- `objectiveAssessments.jsonl`: Section-level objective assessments (EBRW and Math, or Critical Reading/Math/Writing)
- `studentAssessments.jsonl`: Student assessment results with scores and performance levels

## Namespace and Descriptors

- **Assessment Namespace**: `uri://collegeboard.org/sat-suite/`
- **Assessment Family**: "SAT Suite"
- **Custom Descriptors**: Assessment-specific score types and performance levels use College Board namespace
- **Standard Descriptors**: Grade levels and academic subjects use Ed-Fi default namespace

## Score Ranges

### PSAT 8/9
- Total: 240-1440
- Each section: 120-720

### PSAT 10 and PSAT/NMSQT
- Total: 320-1520
- Each section: 160-760

### SAT (Current)
- Total: 400-1600
- Each section: 200-800

### SAT (Pre-2016)
- Total: 600-2400
- Each section: 200-800

## Notes

- The bundle handles year-over-year format changes (old SAT to new SAT)
- Students may take any test at any grade level - grade is calculated, not assumed
- CCR benchmarks are used to assign performance levels when available
- Test type detection is automatic but can be overridden with `TEST_TYPE` parameter

## See Also

- [College Board SAT Suite](https://satsuite.collegeboard.org/)
- [Ed-Fi Assessment Domain](https://edfi.atlassian.net/wiki/spaces/EFDS33/pages/22318436/Assessment+Domain)
- [Earthmover Documentation](https://github.com/edanalytics/earthmover)
