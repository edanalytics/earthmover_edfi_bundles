# ASVAB Data Requirements

This file explains what your ASVAB data needs to look like to be processed correctly.

## Required Columns

Your file must include these columns:

### Student Identification
- `student_unique_id` - Student unique identifier

### Test Information
- `Test Date` - The test date

## Data Format Requirements

### Test Date
**Format:** M/D/YYYY

**Examples:**
- `11/21/2023` for November 21, 2023
- `3/5/2024` for March 5, 2024
- `10/12/2023` for October 12, 2023

**❌ Will NOT work:**
- `11-21-2023` (dashes instead of slashes)
- `2023-11-21` (ISO format)
- `November 21, 2023` (text)

### Grade
**Optional field - can be left blank**

**Valid values if provided:**
- `PK` - Prekindergarten
- `K` - Kindergarten
- `1` through `12` - Numeric grade levels

**Examples:**
- Student in 10th grade: use `10`
- Student in 12th grade: use `12`
- Kindergarten student: use `K`

## Optional Columns

All score columns are optional and can be left blank. If included, they will be sent as score results:

### Top-Level Scores
- `Session Number` - Session identifier
- `Test Version` - Version of the test
- `AFQT Score` - Armed Forces Qualification Test score
- `Career Intent` - Student's career intent
- `Release Option` - Release option selected

### Subject Area Scores
- `MA` - Mathematics Knowledge
- `TEC` - Technical
- `GS` - General Science
- `AR` - Arithmetic Reasoning
- `VE` - Verbal Expression
- `WK` - Word Knowledge
- `PC` - Paragraph Comprehension
- `MK` - Mechanical Comprehension
- `EI` - Electronics Information
- `AS` - Auto & Shop Information
- `MC` - Mathematics Computation

**Note:** Score columns must exist in the file header, but the values can be empty. Only scores with values will be included in the output.
