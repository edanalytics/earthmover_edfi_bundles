# ASVAB Data Requirements

This file explains what your ASVAB data needs to look like to be processed correctly.

## Required Columns

Your file must include these columns:

### Student Identification
- `student_unique_id` - Student unique identifier. Every row must have a value.

### Test Information
- `Test Date` - The test date. Every row must have a value.
- `Grade` - Student grade level. Must exist as a column header, but values can be empty.
- `AFQT` - Armed Forces Qualification Test score. Must exist as a column header, but values can be empty.

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

All other score columns are optional and do not need to appear in your file at all. If present, their values will be processed; if absent or empty, they are skipped.

- `Session Number` - Session identifier
- `Test Version` - Version of the test
- `AFQT Score` - AFQT score (alternate column name)
- `Career Intent` - Student's career intent
- `Release Option` - Release option selected
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
