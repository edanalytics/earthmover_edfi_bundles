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
- `CATEGORY` - Category type

### Score Information
- `PREDICTED_GRADE` - Predicted grade
- `SUBJECT_GRADE` - Subject grade achieved
- `EE_TOK_BONUS_POINTS` - Extended Essay/Theory of Knowledge bonus points
- `TOTAL_POINTS` - Total points earned
- `RESULT_CODE` - Diploma result code

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

### Language (`LANGUAGE`)
**Format:** Language name in uppercase

**Examples:**
- `ENGLISH`
- `SPANISH`
- `FRENCH`

### Category (`CATEGORY`)
**Valid values:**
- `DIPLOMA` - Full IB Diploma Programme
- `CERTIFICATE` - IB Certificate for individual courses

**Note:** The category determines which additional scores are included. DIPLOMA category records include Extended Essay/TOK bonus points, total points, and diploma result codes.

### Predicted Grade (`PREDICTED_GRADE`)
**Format:** Number 1-7, or empty

**Examples:**
- `6`
- `7`
- `5`
- (leave blank if not available)

### Subject Grade (`SUBJECT_GRADE`)
**Format:** Number 1-7

**Examples:**
- `6`
- `7`
- `4`

### EE/TOK Bonus Points (`EE_TOK_BONUS_POINTS`)
**Format:** Number 0-3, or empty

**Examples:**
- `2`
- `1`
- `0`
- (leave blank for non-DIPLOMA records)

**Note:** Only applies to DIPLOMA category records.

### Total Points (`TOTAL_POINTS`)
**Format:** Number, or empty

**Examples:**
- `38`
- `42`
- `28`
- (leave blank for non-DIPLOMA records)

**Note:** Only applies to DIPLOMA category records.

### Result Code (`RESULT_CODE`)
**Format:** Single letter code, or empty

**Valid values for DIPLOMA:**
- `D` - Diploma awarded
- `N` - Diploma not awarded

**Note:** Only applies to DIPLOMA category records.

### Candidate (`CANDIDATE`)
**Format:** Candidate identifier

**Examples:**
- `xyz001`
- `abc123`

## Optional Columns

All other columns in your export file are optional and can be included if present, including:
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

These columns will be ignored during processing.
