# International Baccalaureate (IB) Data Requirements

This file explains what your IB assessment data needs to look like to be processed correctly.

## Required Columns

Your file must include these columns:

### Student Identification
- `student_unique_id` - Student unique identifier

### Test Administration
- `YEAR` - Year of exam administration
- `MONTH` - Month of exam administration
- `CANDIDATE` - Candidate number

### Assessment Information
- `SUBJECT` - Subject name
- `LEVEL` - Course level
- `GROUP_NUMBER` - Subject group number
- `LANGUAGE` - Language of instruction
- `SUBJECT_GRADE` - Subject grade achieved

## Data Format Requirements

### Year (`YEAR`)
**Format:** Four-digit year

**Examples:**
- `2024`
- `2023`
- `2025`

**❌ Will NOT work:**
- `24` (two digits)
- `2024-2025` (range)

### Month (`MONTH`)
**Must be exactly:** `MAY` or `NOV` (uppercase)

**❌ Will NOT work:**
- `May` (lowercase)
- `05` (numeric)
- `NOVEMBER` (full name)

### Group Number (`GROUP_NUMBER`)
**Cannot be empty - must have a value**

**Valid values:**
- `1` - Studies in Language and Literature (non-English)
- `1 - English` - Studies in Language and Literature (English)
- `1 - Foreign Language` - Language Acquisition
- `2` - Language Acquisition
- `3 and 4` - Individuals and Societies / Sciences
- `5` - Mathematics
- `6` - Arts
- `9` - Theory of Knowledge and other special subjects

**Note:** This field is critical for categorizing subjects and cannot be left blank.

### Subject (`SUBJECT`)
**Format:** Text name of the subject

**Examples:**
- `ENV. AND SOC.`
- `MATH ANALYSIS`
- `BIOLOGY`
- `ENGLISH A: LIT`

### Level (`LEVEL`)
**Valid values:**
- `SL` - Standard Level
- `HL` - Higher Level
- `TK` - Theory of Knowledge

### Language (`LANGUAGE`)
**Format:** Language name in uppercase

**Examples:**
- `ENGLISH`
- `SPANISH`
- `FRENCH`

### Subject Grade (`SUBJECT_GRADE`)
**Format:** Number 1-7, or a letter grade for special subjects

**Examples:**
- `6`
- `7`
- `B` (for Theory of Knowledge)
- `N` (Not graded/No grade awarded)

### Candidate (`CANDIDATE`)
**Format:** Candidate identifier

**Examples:**
- `xyz001`
- `abc123`

## Optional Columns

These columns do not need to appear in your file at all. If present, their values will be processed; if absent or empty, they are skipped.

- `CATEGORY` - Category type (DIPLOMA or CERTIFICATE)
- `PREDICTED_GRADE` - Predicted grade
- `EE_TOK_BONUS_POINTS` - Extended Essay/Theory of Knowledge bonus points
- `TOTAL_POINTS` - Total points earned
- `RESULT_CODE` - Diploma result code
- `PROGRAMME`
- `REGIONAL_OFFICE`
- `COUNTRY`
- `STATE`
- `SCHOOL_CODE`
- `SCHOOL_NAME`
- `LEGAL_STATUS`
- `FIRST_NAME`
- `LAST_NAME`
- `DOB`
- `GENDER`
- `GROUP_OF_SCHOOLS`
