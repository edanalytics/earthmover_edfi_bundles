# ACT Data Requirements

This file explains what your ACT data needs to look like to be processed correctly.

## Columns That Must Have Values

These columns must be present **and** contain data for every row.

### Student Identification
- Your student ID column (e.g., `ID_StateAssign` or `ID_Local`). Every row must have a student ID value.
- `ID_ACT` - The ACT student ID number. Every row must have this value.

### Test Information
- `Test_Dte` - The test date. Every row must have a value.
- `HS_GradeLev` - The student's high school grade level. Every row must have a valid value (see format requirements below). Records with blank or unrecognized grade values will be excluded.

### At Least One Composite Score
At least one of these must have a non-dash value in each row:
- `Composite`
- `StRnk_Comp`
- `USRnk_Comp`
- `Sup_Composite`
- `Sum_Scale`
- `Sup_Sum_Scale`

If all of these are dashes or empty for a row, that record will be excluded.

These columns do not all need to be present in your file — only the ones you have data for.

## Columns That Must Exist (Values Can Be Empty)

These columns must appear as **headers** in your file, but individual rows can have blank values.

### College Readiness
- `C_Readiness` - College readiness indicator. If blank, the performance level is simply skipped for that row.

## Data Format Requirements

### Test Date (`Test_Dte`)
**Format:** 6-digit number as MMYYYY

**Examples:**
- `092024` for September 2024
- `102024` for October 2024
- `042025` for April 2025

**❌ Will NOT work:**
- `09/2024` (contains slash)
- `2024-09` (wrong order)
- `September 2024` (text)

### Grade Level (`HS_GradeLev`)
**Must be exactly one of these values:**
- `6th or 7th Grade`
- `8th Grade`
- `9th Grade`
- `10th Grade`
- `11th Grade`
- `12th Grade`
- `H.S. Graduate`
- `College Student`
- `Other`

Records with any other value (like "Grade 11" or "Junior") or blank values will be excluded.

### College Readiness (`C_Readiness`)
Valid values:
- `0` = Unlikely to obtain an NCRC
- `1` = Likely to obtain a Bronze level NCRC
- `2` = Likely to obtain a Silver level NCRC
- `3` = Likely to obtain a Gold level NCRC
- `4` = Likely to obtain a Platinum level NCRC

Other values or blank will not produce a performance level for that row.

### Score Columns
**For missing or unavailable scores:** Use dashes (`-`, `--`, `---`) or leave blank.

**For valid scores:** Use numbers, like `16`, `21`, `28`.

**❌ Do NOT use:**
- Text like "N/A" or "Not Available"

## Optional Columns

These columns do not need to appear in your file at all. If present, their values will be processed; if absent or empty, they are skipped.

- Subject scores (English, Math, Reading, Science, Writing)
- Subject ranks and superscores
- STEM and ELA scores
- All subscore columns (points earned, points possible, percent correct, readiness ranges)
