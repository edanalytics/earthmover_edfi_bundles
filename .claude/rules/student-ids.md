# Student ID Crosswalking (Xwalking)

This document explains the student ID crosswalking feature for matching assessment vendor IDs to Ed-Fi roster IDs.

## Overview

Student ID crosswalking (xwalking) is an **optional advanced feature** for scenarios where:
- Assessment vendor uses different student IDs than Ed-Fi ODS
- No direct mapping exists between vendor IDs and Ed-Fi studentUniqueId
- Probabilistic matching is needed (name + DOB + demographics)

**Common scenarios:**
- State assessment IDs ≠ district Ed-Fi IDs
- Vendor uses SSID, district uses local ID
- Historical assessments with deprecated ID systems

## Two-Package System

The xwalking implementation uses two earthmover packages in sequence:

### 1. compute_match_rates Package

**Purpose:** Analyzes potential matches between assessment IDs and Ed-Fi roster IDs.

**Inputs:**
- Assessment file with vendor student IDs
- Ed-Fi roster with studentUniqueId
- Student demographics (name, DOB, etc.)

**Output:**
- Match rate report showing confidence levels
- Candidate matches with scores

**Located at:** `packages/student_ids/compute_match_rates/`

### 2. apply_xwalk Package

**Purpose:** Applies the best matches to replace vendor IDs with Ed-Fi IDs.

**Inputs:**
- Assessment file with vendor student IDs
- Match results from compute_match_rates
- Threshold configuration

**Output:**
- Assessment data with Ed-Fi studentUniqueId column (`edFi_studentUniqueID`)

**Located at:** `packages/student_ids/apply_xwalk/`

## How It Works

### Standard Flow (No Xwalking)

When vendor ID = Ed-Fi ID:

```yaml
# earthmover.yaml
sources:
  input:
    file: ${INPUT_FILE}
transformations:
  assessments:
    source: $sources.input
    operations: []  # Empty - no xwalking needed
```

Template uses:
```jinja
"studentReference": {
  "studentUniqueId": "${edFi_studentUniqueID}"
}
```

Parameter: `STUDENT_ID_NAME=edFi_studentUniqueID` (default)

### Xwalking Flow

When vendor ID ≠ Ed-Fi ID:

```yaml
# earthmover.yaml (user modifies)
sources:
  input:
    file: ${INPUT_FILE}

  roster:
    file: ${ROSTER_FILE}  # Ed-Fi roster with demographics

transformations:
  # 1. Compute matches
  match_rates:
    source: $sources.input
    operations:
      - operation: join
        sources:
          - $sources.roster
        join_type: left
        left_key: ${vendor_student_id_column}
        right_key: studentUniqueId
      # ... match logic from package

  # 2. Apply best matches
  assessments:
    source: $transformations.match_rates
    operations:
      - operation: add_column
        column_name: edFi_studentUniqueID
        value: ${matched_id_from_xwalk}
```

Template unchanged (still uses `${edFi_studentUniqueID}`).

## Bundle Implementation Requirements

### ✓ Empty Initial Transformation

Bundles must start with an empty transformation to support xwalking:

```yaml
transformations:
  assessments:
    source: $sources.input
    operations: []  # Empty - allows packages to insert xwalking logic
```

**Why:** The xwalking packages insert their operations here. A bundle with operations already defined would conflict.

### ✓ STUDENT_ID_NAME Parameter

```yaml
# earthmover.yaml
parameters:
  STUDENT_ID_NAME: edFi_studentUniqueID  # Default
```

**Usage:**
- Standard case: User doesn't override, uses default column name
- Xwalking case: Xwalking package creates `edFi_studentUniqueID` column
- Template always references: `${edFi_studentUniqueID}`

**DO NOT:**
- Hard-code column name in template
- Use vendor column name directly
- Assume column exists without parameter

### ✓ Template Column Reference

```jinja
"studentReference": {
  "studentUniqueId": "${edFi_studentUniqueID}"
}
```

**Always use the parameter-defined column name.**

## Matching Methodology

### Deterministic Match

Perfect match on unique identifier:
- Vendor ID exists in Ed-Fi roster
- 100% confidence
- No ambiguity

### Probabilistic Match

Match based on demographic similarity:
- Last name (phonetic match)
- First name (phonetic match)
- Date of birth
- Gender
- Race/ethnicity
- School/grade

**Match score:** Calculated based on field weights.

**Threshold:** User-configurable (typically 0.8 or higher).

### Unmatched Records

Records below threshold:
- Can be manually reviewed
- May require district to provide mapping
- Can be excluded from integration

## Package Documentation

### Detailed Implementation

See `packages/student_ids/README.md` for:
- Complete package usage instructions
- Match algorithm details
- Configuration options
- Troubleshooting guide

### Package Composition

Xwalking is applied by composing packages into the bundle:

```yaml
# earthmover.yaml (user-modified)
sources:
  input:
    file: ${INPUT_FILE}

  roster:
    file: ${ROSTER_FILE}

packages:
  - packages/student_ids/compute_match_rates/
  - packages/student_ids/apply_xwalk/

transformations:
  # Packages inject their transformations here
  assessments:
    source: $transformations.xwalked_students  # Output from packages
    operations:
      - operation: rename_columns
        columns:
          # Bundle-specific mappings
```

## When to Use Xwalking

### ✓ Use When:
- Vendor IDs don't match Ed-Fi IDs
- District has roster with demographics
- Probabilistic matching is acceptable
- Match rate analysis is needed

### ✗ Don't Use When:
- Vendor ID = Ed-Fi ID (standard case)
- No roster available for matching
- 100% deterministic match required
- Simple ID mapping exists (use lookup table instead)

## Testing Xwalking

### 1. Test Standard Case First

Before adding xwalking, verify bundle works with standard ID flow:

```bash
earthmover run -c earthmover.yaml -p '{"INPUT_FILE": "data/sample.csv", "API_YEAR": 2024}'
```

Should produce valid output with vendor IDs as studentUniqueId.

### 2. Test With Xwalking

Add xwalking packages and roster:

```bash
earthmover run -c earthmover.yaml -p '{
  "INPUT_FILE": "data/sample.csv",
  "ROSTER_FILE": "data/roster.csv",
  "API_YEAR": 2024
}'
```

**Verify:**
- Match rate report generated
- `edFi_studentUniqueID` column created
- Output has Ed-Fi IDs, not vendor IDs
- Unmatched records handled appropriately

### 3. Review Match Quality

Check match rate report:
- What percentage matched?
- What's the confidence distribution?
- Are unmatched records explainable?

**Target:** 95%+ match rate for good data quality.

## Common Xwalking Mistakes

### ❌ Hard-Coding Vendor Column in Template

**Wrong:**
```jinja
"studentUniqueId": "${vendor_student_id}"
```

**Correct:**
```jinja
"studentUniqueId": "${edFi_studentUniqueID}"
```

### ❌ Operations in Initial Transformation

**Wrong:**
```yaml
transformations:
  assessments:
    source: $sources.input
    operations:
      - operation: rename_columns  # Blocks xwalking package insertion
        columns: {...}
```

**Correct:**
```yaml
transformations:
  assessments:
    source: $sources.input
    operations: []  # Empty for xwalking compatibility
```

### ❌ Assuming Xwalking Always Needed

**Wrong:** Implementing xwalking when vendor ID = Ed-Fi ID.

**Correct:** Use standard flow as default; xwalking is optional when needed.

### ❌ Not Testing Standard Case

**Wrong:** Only testing with xwalking enabled.

**Correct:** Test standard case first, then add xwalking if needed.

## Documentation for Bundle Users

### README.md Section

Include in bundle README:

```markdown
## Student ID Crosswalking (Optional)

This bundle supports optional student ID crosswalking for scenarios where assessment IDs don't match Ed-Fi roster IDs.

**Standard usage (IDs match):**
```bash
earthmover run -c earthmover.yaml -p '{"INPUT_FILE": "data/sample.csv", "API_YEAR": 2024}'
```

**With crosswalking (IDs don't match):**

Requires the xwalking packages from `packages/student_ids/`. See `packages/student_ids/README.md` for complete instructions.
```

## References

- **Package README:** `packages/student_ids/README.md`
- **Slite Workflow:** "Writing earthmover bundles" (step 10: Student ID xwalking)
- **Example Bundles:** Check existing bundles for xwalking implementation patterns
