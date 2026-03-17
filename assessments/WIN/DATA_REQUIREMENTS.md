# WIN (Workplace Innovator) Data Requirements

This file explains what your WIN assessment data needs to look like to be processed correctly.

## Required Columns

Your file must include these columns:

### Student Identification
- `StudentID` - Local student ID
- `StateID` - State student ID

### School Information
- `SchoolID` - School identifier

### Test Administration
- `TestAdmin` - Test administration period
- `TestDate` - Test date
- `Mode` - Testing mode

### Test Details
- `Acc` - Accommodations indicator
- `Retake` - Retake indicator
- `CertLevel` - Certificate level
- `UID` - Unique identifier (can be left blank)

### Soft Skills Assessment (Required)
- `SoftScore` - Soft skills score
- `SoftSS` - Soft skills scale score
- `SoftStatus` - Soft skills status
- `SoftSTime` - Soft skills start time
- `SoftFTime` - Soft skills finish time

### Math Assessment (Required)
- `MathLev` - Math level
- `MathSS` - Math scale score
- `MathStatus` - Math status
- `MathSTime` - Math start time
- `MathFTime` - Math finish time

### Reading Assessment (Required)
- `ReadLev` - Reading level
- `ReadSS` - Reading scale score
- `ReadStatus` - Reading status
- `ReadSTime` - Reading start time
- `ReadFTime` - Reading finish time

### Data Literacy Assessment (Optional)
These columns must exist in the file header but can have empty values:
- `DataLev` - Data literacy level
- `DataSS` - Data literacy scale score
- `DataStatus` - Data literacy status
- `DataSTime` - Data literacy start time
- `DataFTime` - Data literacy finish time

### Information Literacy Assessment (Optional)
These columns must exist in the file header but can have empty values:
- `InfoLev` - Information literacy level
- `InfoSS` - Information literacy scale score
- `InfoStatus` - Information literacy status
- `InfoSTime` - Information literacy start time
- `InfoFTime` - Information literacy finish time

## Data Format Requirements

### Test Date (`TestDate`)
**Format:** YYYYMMDD (8-digit number)

**Examples:**
- `20231101` for November 1, 2023
- `20240315` for March 15, 2024
- `20251210` for December 10, 2025

**❌ Will NOT work:**
- `11/01/2023` (slashes)
- `2023-11-01` (dashes)
- `20231101` missing leading zeros

### Test Administration (`TestAdmin`)
**Format:** Two-letter season code followed by two-digit year

**Examples:**
- `FA23` for Fall 2023
- `SP24` for Spring 2024
- `FA24` for Fall 2024

**Valid season codes:**
- `FA` - Fall
- `SP` - Spring

### Mode (`Mode`)
**Format:** Single letter code

**Examples:**
- `O` - Online
- `P` - Paper

### Accommodations (`Acc`)
**Format:** Number

**Valid values:**
- `1` - Yes (accommodations provided)
- `0` - No (no accommodations)

### Retake (`Retake`)
**Format:** Single letter

**Valid values:**
- `Y` - Yes (this is a retake)
- `N` - No (first attempt)

### Soft Skills Score (`SoftScore`)
**Format:** Number

**Valid values:**
- `1` - Pass
- `0` - Fail

### Status Fields
**For `MathStatus`, `ReadStatus`, `SoftStatus`, `DataStatus`, `InfoStatus`:**

**Valid values:**
- `1` - Complete
- `0` - Incomplete

### Time Fields
**For all time fields (STime and FTime):**

**Format:** 24-hour time without separator (e.g., HHMM)

**Examples:**
- `907` for 9:07 AM
- `1045` for 10:45 AM
- `1330` for 1:30 PM

**Note:** Times are used to calculate duration. Start and finish times are required for Math, Reading, and Soft Skills assessments. For Data and Info assessments, times can be empty if those assessments were not administered.

### Unique Identifier (`UID`)
**Optional field - can be left blank**

If not provided, the system will generate an identifier using TestAdmin, TestDate, and StudentID.

## Important Notes

- All columns listed above must be present in your file header, even if some values are empty
- Data Literacy and Information Literacy assessments are optional - these columns can have all empty values if those assessments were not administered
- Math, Reading, and Soft Skills assessments are required and must have values
