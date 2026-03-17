# SAT/PSAT Data Requirements

This file explains what your SAT or PSAT data needs to look like to be processed correctly.

**Note:** For PSAT, replace `SAT` with `PSAT` in all column names below.

## Columns That Must Have Values

These columns must be present **and** contain data for every row.

### Student Identification
Your student ID column (e.g., `STATE_STUDENT_ID`, `DISTRICT_STUDENT_ID`, or `SECONDARY_ID`). Every row must have a student ID value.

### Test Date
- `LATEST_SAT_DATE` - Every row must have a test date.

### Total Score
At least one of these must have a value in each row:
- `LATEST_SAT_TOTAL` - Total composite score
- `PERCENTILE_NATUSER_SAT_TOTAL` - User percentile for total score
- `PERCENTILE_NATREP_SAT_TOTAL` - Nationally representative percentile for total score

If all three are blank for a row, that record will produce invalid output.

## Columns That Must Exist (Values Can Be Empty)

These columns must appear as **headers** in your file, but individual rows can have blank values. If a value is blank, that score or section is simply skipped.

### Grade Level
- `LATEST_SAT_GRADE` - Grade level when assessed. Blank values are treated as "No grade level."

### Composite Percentiles
- `PERCENTILE_NATUSER_SAT_TOTAL` - User percentile for total score
- `PERCENTILE_NATREP_SAT_TOTAL` - Nationally representative percentile for total score

(These are also listed above because at least one composite score must have a value per row, but they can individually be blank.)

### EBRW (Evidence-Based Reading and Writing) Section
- `LATEST_SAT_EBRW` - Section score
- `PERCENTILE_NATREP_SAT_EBRW` - Nationally representative percentile
- `PERCENTILE_NATUSER_SAT_EBRW` - User percentile
- `EBRW_CCR_BENCHMARK` - College and career readiness benchmark indicator

If all EBRW values are blank, the EBRW section is skipped for that row.

### Math Section
- `LATEST_SAT_MATH_SECTION` - Section score
- `PERCENTILE_NATREP_SAT_MATH_SECTION` - Nationally representative percentile
- `PERCENTILE_NATUSER_SAT_MATH_SECTION` - User percentile
- `MATH_CCR_BENCHMARK` - College and career readiness benchmark indicator

If all Math values are blank, the Math section is skipped for that row.

### Essay (SAT Only)
- `LATEST_SAT_ESSAY_READING` - Essay reading subscore
- `LATEST_SAT_ESSAY_ANALYSIS` - Essay analysis subscore
- `LATEST_SAT_ESSAY_WRITING` - Essay writing subscore

These column headers are only needed for SAT files (not PSAT). The digital SAT (2024+) does not include an essay, so these will typically be blank for recent test dates.

## Data Format Requirements

### Test Date
**Two formats are supported:**

1. **M/D/YYYY format** (recommended)
   - `10/12/2015` for October 12, 2015
   - `3/5/2024` for March 5, 2024

2. **YYYY-MM-DD format** (ISO format)
   - `2015-10-12` for October 12, 2015
   - `2024-03-05` for March 5, 2024

**❌ Will NOT work:**
- `10-12-2015` (dashes in M-D-Y format)
- `2015/10/12` (slashes in wrong order)
- `October 12, 2015` (text)

### Grade Level
**Must be a numeric code:**

Valid values:
- `1` = Other
- `2` = Eighth grade
- `4` = Ninth grade
- `5` = Tenth grade
- `6` = Eleventh grade
- `7` = Twelfth grade
- `8` = Out of School
- `10` or `11` = No grade level
- `12` or `13` = Postsecondary
- (blank/empty) = No grade level

**Examples:**
- Student in 11th grade: use `6`
- Student in 12th grade: use `7`
- Recent graduate: use `8`

Records with grade values that don't match these codes (e.g., `3`, `9`) will be excluded.

### Benchmark Indicators
**For `EBRW_CCR_BENCHMARK` and `MATH_CCR_BENCHMARK`:**

Valid values:
- `Y` = Student met the benchmark
- `N` = Student did not meet the benchmark
- (blank/empty) = Benchmark is skipped for that row

### Score Values
**For all score columns** (section scores, percentiles, subscores):

- **Valid scores:** Use numbers, like `670`, `89`, `32`
- **Missing scores:** Leave blank or empty

**❌ Do NOT use:**
- Dashes (`-`, `--`, `---`)
- Text like "N/A" or "Not Available"
- Zero for missing values (unless the actual score is zero)

## Optional Columns

These columns do not need to appear in your file at all. If present, their values will be processed; if absent or empty, they are skipped.

- Test scores (Reading, Writing/Language, Math Test)
- Subscores (Words in Context, Command of Evidence, Heart of Algebra, etc.)
- Cross-test scores (Science, History/Social Studies)
- Question-level details (number correct/incorrect/omitted)
- Percentile details for subscores
