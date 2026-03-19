# Sample Data Handling Guide

This guide covers the proper handling of assessment sample files, which often contain PII (Personally Identifiable Information).

## Critical Safety Rules

### ⚠️ NEVER Copy, Move, or Modify Original Sample Files

Sample files provided for bundle development typically contain **real student data with PII**. These files must be handled with extreme care:

**NEVER:**
- ❌ Copy sample files into the repository
- ❌ Move sample files from their original location
- ❌ Modify sample files in place
- ❌ Commit sample files to git
- ❌ Upload sample files to cloud storage
- ❌ Share sample files via email, Slack, or other channels

**ALWAYS:**
- ✅ Keep sample files in their original secure location
- ✅ Read sample files in place (read-only mode)
- ✅ Generate anonymized versions for the repository
- ✅ Verify anonymized files contain NO PII before committing

### Why This Matters

PII exposure can result in:
- Legal compliance violations (FERPA, state privacy laws)
- Breach of vendor agreements
- Loss of district/state trust
- Potential harm to students and families
- Data security incidents

**When in doubt, treat ALL sample files as containing PII until proven otherwise.**

## Sample File Workflow

### Step 1: Receive Sample Files

Sample files are typically provided:
- Via secure file share (OneDrive, SharePoint, etc.)
- In a secure network location
- Directly from vendor or district partner

**Location conventions:**
- Samples may be stored in a separate secure directory outside the repository
- Samples are NEVER part of the earthmover_edfi_bundles repository
- Samples should remain in their original location

### Step 2: Examine Sample Files

**Purpose:** Understand assessment structure, file format, and data coverage.

**Key questions to answer:**
1. What columns are present?
2. What assessment structure is represented? (subject-level, test-level, item-level)
3. What score types are included?
4. What performance levels exist?
5. Are there objective assessments (subscores, domains)?
6. How is the hierarchy structured?
7. What grade levels are covered?
8. What date formats are used?
9. Are there null values? How are they represented?

**If multiple samples provided:**
- Check for format changes year-over-year
- Note which columns appear/disappear across years
- Identify format variations (e.g., date formats, delimiter changes)
- Determine if separate bundles are needed for different formats

### Step 3: Document Assessment Structure

Before creating governance artifact or bundle:

**Create assessment structure notes:**
```
Assessment: [Name]
Sample files examined:
  - file1.csv (SY 2023-24)
  - file2.csv (SY 2024-25)

Structure:
- Split by subject: [Yes/No]
- Hierarchy: [Description]
- Score types: [List]
- Performance levels: [List]
- Objective assessments: [List]

Format notes:
- One row per: [student test | item response | domain score]
- Date format: [YYYY-MM-DD | MM/DD/YYYY | etc.]
- Null representation: [empty string | "NULL" | -999]

Year-over-year changes:
- SY 2023-24: [Format A]
- SY 2024-25: [Added columns X, Y; removed column Z]
```

### Step 4: Generate Anonymized Sample Files

**Purpose:** Create representative test data for bundle development WITHOUT PII.

#### Anonymization Rules

**Student identifiers:**
- Replace with synthetic IDs: `999900001`, `999900002`, etc.
- Use sequential numbers in 9999XXXXX range
- Keep consistent across rows for same student

**Names:**
- Replace with generic names: "Student A", "Student B", etc.
- Or remove name columns entirely if not needed

**Dates of birth:**
- Replace with generic dates: "2010-01-01", "2010-01-02", etc.
- Or use year only: "2010", "2011", etc.

**School/District identifiers:**
- Replace with generic: "School A", "District X"
- Or use codes: "SCH001", "DIST001"

**Teacher/Staff names:**
- Remove entirely or replace with "Teacher A", "Teacher B"

**Addresses, phone numbers, emails:**
- Remove entirely - not needed for assessment bundles

**Assessment data (scores, performance levels):**
- KEEP REALISTIC VALUES - these are needed for testing
- Ensure coverage of all score ranges
- Include examples of null/missing values
- Include examples of all performance levels

#### Anonymization Process

**Option 1: Manual Anonymization (Small Files)**

```python
import pandas as pd

# Read original sample (READ ONLY - DO NOT MODIFY)
df = pd.read_csv('/secure/location/original_sample.csv')

# Create anonymized copy
df_anon = df.copy()

# Replace PII columns
df_anon['student_id'] = [f'99990{i:04d}' for i in range(len(df_anon))]
df_anon['student_name'] = [f'Student {chr(65 + i % 26)}' for i in range(len(df_anon))]
df_anon['date_of_birth'] = '2010-01-01'
df_anon['school_name'] = 'Example School'

# Drop columns not needed
df_anon = df_anon.drop(columns=['teacher_name', 'email'], errors='ignore')

# Verify no PII remains
print(df_anon.head(20))  # REVIEW CAREFULLY

# Save to repository data/ directory
df_anon.to_csv('assessments/YOUR_BUNDLE/data/sample_anonymized.csv', index=False)
```

**Option 2: Sampling + Anonymization (Large Files)**

```python
import pandas as pd

# Read original sample
df = pd.read_csv('/secure/location/original_sample.csv')

# Sample subset of rows (e.g., 100 students)
df_sample = df.sample(n=100, random_state=42)

# Anonymize (same as above)
df_anon = df_sample.copy()
df_anon['student_id'] = [f'99990{i:04d}' for i in range(len(df_anon))]
# ... (continue anonymization)

# Save
df_anon.to_csv('assessments/YOUR_BUNDLE/data/sample_anonymized.csv', index=False)
```

**Option 3: Synthetic Data Generation (If Real Data Too Sensitive)**

```python
import pandas as pd
import numpy as np

# Create synthetic data matching original structure
n_students = 50

df_synthetic = pd.DataFrame({
    'student_id': [f'99990{i:04d}' for i in range(n_students)],
    'test_date': '2024-10-15',
    'grade_level': np.random.choice(['03', '04', '05'], n_students),
    'scale_score': np.random.randint(400, 600, n_students),
    'performance_level': np.random.choice(['Below Basic', 'Basic', 'Proficient', 'Advanced'], n_students),
    # ... add all columns matching original structure
})

# Save
df_synthetic.to_csv('assessments/YOUR_BUNDLE/data/sample_synthetic.csv', index=False)
```

### Step 5: Verify Anonymized Files

**Critical verification before committing:**

```bash
# Check for common PII indicators
grep -i "gmail\|yahoo\|@" assessments/YOUR_BUNDLE/data/*.csv
grep -i "smith\|johnson\|williams" assessments/YOUR_BUNDLE/data/*.csv  # Common surnames
grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}" assessments/YOUR_BUNDLE/data/*.csv  # SSN pattern
grep -E "[0-9]{3}-[0-9]{3}-[0-9]{4}" assessments/YOUR_BUNDLE/data/*.csv  # Phone pattern

# Manual review
head -20 assessments/YOUR_BUNDLE/data/sample_anonymized.csv
```

**Verification checklist:**
- [ ] No real student names
- [ ] No real student IDs (check IDs don't match actual patterns)
- [ ] No real school names (unless generic public info)
- [ ] No real district names
- [ ] No addresses
- [ ] No phone numbers
- [ ] No email addresses
- [ ] No dates of birth (or only generic dates)
- [ ] File size is reasonable (<1MB for sample data)
- [ ] Covers all assessment scenarios (all grades, all performance levels, etc.)

### Step 6: Document Sample Source

In bundle README, document sample file provenance WITHOUT including the original file:

```markdown
## Sample Data

The anonymized sample file in `data/sample_anonymized.csv` was generated from:
- Source: [Vendor Name] assessment files
- Years examined: SY 2023-24, SY 2024-25
- Original file structure: One row per student assessment
- Anonymization: Student IDs replaced with 9999XXXXX range, all PII removed

This file is representative of the vendor's standard file format and includes examples of all score types and performance levels.
```

## Handling Multiple Sample Files

### Year-over-Year Format Changes

**When samples show format differences:**

1. **Document all variations:**
   ```
   SY 2023-24 format:
   - Columns: student_id, test_date, scale_score, percentile
   - Date format: MM/DD/YYYY

   SY 2024-25 format:
   - Columns: student_id, test_date, scale_score, percentile, performance_level
   - Date format: YYYY-MM-DD
   - Added: performance_level column
   ```

2. **Decide on bundle strategy:**
   - **Single bundle with conditionals** if changes are minor (e.g., added optional column)
   - **Separate bundles** if changes are major (e.g., different structure, different hierarchy)

3. **Create anonymized samples for each format:**
   ```
   assessments/YOUR_BUNDLE/data/
     sample_2023_format.csv
     sample_2024_format.csv
   ```

4. **Use year-based logic in earthmover:**
   ```yaml
   transformations:
     assessments:
       source: $sources.input
       operations:
         {% if ${API_YEAR} >= 2024 %}
         - operation: add_column
           column_name: performance_level
           value: ${performance_level}
         {% endif %}
   ```

### Multiple Assessment Types

**When vendor provides multiple assessment types:**

Example: STAR provides STAR-SR (reading), STAR-Math, STAR-EL (early literacy)

1. **Examine all samples:**
   - STAR-SR sample
   - STAR-Math sample
   - STAR-EL sample

2. **Determine bundle structure:**
   - Separate bundles if structures differ significantly
   - Single bundle if structure is identical (just different subjects)

3. **Create anonymized samples for each:**
   ```
   assessments/STAR-SR/data/sample.csv
   assessments/STAR-Math/data/sample.csv
   assessments/STAR-EL/data/sample.csv
   ```

## Common Mistakes to Avoid

### ❌ Copying Sample Files "Just for Reference"

**Wrong:**
```bash
# DO NOT DO THIS
cp /secure/samples/vendor_assessment_2024.csv assessments/NEW_BUNDLE/data/
```

**Right:**
```bash
# Read in place, generate anonymized
python anonymize_sample.py /secure/samples/vendor_assessment_2024.csv
# Saves to assessments/NEW_BUNDLE/data/sample_anonymized.csv
```

### ❌ Insufficient Anonymization

**Wrong:**
```python
# Real student IDs that match actual district patterns
df_anon['student_id'] = df['student_id']  # Original IDs preserved
```

**Right:**
```python
# Synthetic IDs in clearly test range
df_anon['student_id'] = [f'99990{i:04d}' for i in range(len(df_anon))]
```

### ❌ Not Checking All Samples

**Wrong:**
```
# Only examining most recent sample
# Missing format change from 2 years ago
```

**Right:**
```
# Examining all provided samples
# Noting format evolution over time
# Testing bundle against all formats
```

### ❌ Including Too Much Data

**Wrong:**
```python
# 100,000 row sample file
df_anon = df  # Full dataset anonymized
```

**Right:**
```python
# 50-100 row sample file
df_anon = df.sample(n=50, random_state=42)  # Representative subset
```

### ❌ Forgetting to Verify

**Wrong:**
```bash
# Generate anonymized file and immediately commit
git add assessments/NEW_BUNDLE/data/sample.csv
git commit -m "Add sample data"
```

**Right:**
```bash
# Generate, review, verify, then commit
head -50 assessments/NEW_BUNDLE/data/sample.csv  # Manual review
grep -i "@" assessments/NEW_BUNDLE/data/sample.csv  # Check for emails
# ... more verification
git add assessments/NEW_BUNDLE/data/sample.csv
git commit -m "Add anonymized sample data"
```

## Integration with Bundle Development Workflow

### Bundle Creation Process

1. **Receive sample files** (kept in secure location)
2. **Examine samples** (read-only, understand structure) ← THIS GUIDE
3. **Generate anonymized samples** (for repository) ← THIS GUIDE
4. **Create governance artifact** (using structure from samples)
5. **Implement bundle** (earthmover.yaml, templates, etc.)
6. **Test with anonymized samples** (local validation)
7. **Test with real samples** (integration testing, samples stay secure)
8. **Commit bundle** (anonymized samples only)

### Using Original Samples for Testing

**During development, you may want to test against original samples:**

```bash
# Test with original sample (NOT in repository)
cd assessments/YOUR_BUNDLE
earthmover run -c earthmover.yaml -p '{
  "INPUT_FILE": "/secure/samples/original_sample.csv",
  "API_YEAR": 2024
}'

# Output goes to output/ (gitignored)
# Original sample remains untouched in secure location
```

**IMPORTANT:**
- Original sample is referenced by path ONLY
- Original sample is NEVER moved or copied
- Output contains derived data (should be safe but gitignore anyway)
- Clean up output after testing: `rm -rf output/`

## Questions to Ask When in Doubt

**Before handling any sample file:**

1. Does this file contain real student names? → **PII**
2. Does this file contain real student IDs? → **Likely PII**
3. Does this file contain dates of birth? → **PII**
4. Does this file contain school/district identifiers that could identify specific students? → **Potential PII**
5. Could someone identify students by combining multiple fields? → **PII by inference**

**If answer is YES to any → Do NOT commit, copy, or move the file.**

## Getting Help

If unsure about PII handling:
- Ask the user before proceeding
- Default to treating data as PII if uncertain
- When in doubt, generate synthetic data instead

If sample files are needed for bundle development:
- Ask user for secure location path
- Read files in place (read-only)
- Generate anonymized versions
- Verify thoroughly before committing

## References

- **FERPA Regulations:** https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html
- **Data Anonymization Best Practices:** https://www.nist.gov/
- **Bundle Development Workflow:** `.claude/rules/governance.md`
- **Quality Checklist (PII Section):** `.claude/rules/quality-checklist.md`
