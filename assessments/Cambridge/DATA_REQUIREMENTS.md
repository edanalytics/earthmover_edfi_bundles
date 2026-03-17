# Cambridge International Data Requirements

This file explains what your Cambridge International assessment data needs to look like to be processed correctly.

## Required Columns

Your file must include these columns:

### Student Identification
- `STUDENT_STATE_ID` - State student ID number

### Test Information
- `SERIES` - Test administration series/date
- `QUALIFICATION` - Type of qualification
- `LEVEL_ENTERED` - Level the student entered for
- `LEVEL_ACHIEVED` - Level the student achieved
- `SYLLABUS` - Syllabus code number
- `SYLLABUS_NAME` - Syllabus name
- `GRADE` - Grade received

## Data Format Requirements

### Series (`SERIES`)
**Format:** DD-MMM (day-month abbreviation)

**Examples:**
- `30-May` for May 30
- `15-Jun` for June 15
- `01-Oct` for October 1

**Valid month abbreviations:**
- `Apr`, `May`, `Jun`, `Sep`, `Oct`, `Nov`

**❌ Will NOT work:**
- `May 30` (wrong format)
- `05/30` (slashes instead of text)
- `30-05` (numbers instead of month name)

### Qualification (`QUALIFICATION`)
**Common values:**
- `AS & A Level` - For AS and A Level exams
- `ADIP` - For AICE Diploma
- `IGCSE` - For IGCSE exams

### Level Achieved (`LEVEL_ACHIEVED`)
**Must have a value - cannot be a dash (`-`)**

**Valid values include:**
- `AS Level`
- `A Level`
- `ADIP` (for AICE Diploma)
- Other qualification levels as appropriate

**❌ Will NOT work:**
- `-` (dash) - Records with dashes will be excluded

**Note:** Records where Level Achieved is a dash will be excluded.

### Level Entered (`LEVEL_ENTERED`)
**Should match the level the student registered for:**
- `AS Level`
- `A Level`
- `ADIP`

### Syllabus (`SYLLABUS`)
**Format:** Numeric code

**Examples:**
- `8021` for English General Paper
- `9702` for Physics
- `ADIP` for AICE Diploma

### Syllabus Name (`SYLLABUS_NAME`)
**Format:** Text name of the subject

**Examples:**
- `ENGLISH GENERAL PAPER`
- `PHYSICS`
- `AICE DIPLOMA`

### Grade (`GRADE`)
**Format:** Letter grade or diploma level

**Examples for AS/A Levels:**
- `A`, `B`, `C`, `D`, `E` - Letter grades
- `a`, `b`, `c`, `d`, `e` - Lowercase also accepted

**Examples for AICE Diploma:**
- `D` - Distinction
- `M` - Merit
- `P` - Pass

## Optional Columns

All other columns in your export file are optional and can be included if present, including:
- `STATE`
- `DISTRICT`
- `CENTRE`
- `CANDIDATE_NUMBER`
- `STUDENT_NAME`
- `ETHNICITY`
- `NATIONAL_ID`
- `SEX`
- `DOB`

These columns will be ignored during processing.
