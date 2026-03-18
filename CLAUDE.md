# Claude Code Instructions for earthmover_edfi_bundles

This file contains project-specific instructions and preferences for Claude Code when working in this repository.

## Project Overview
This repository contains earthmover bundles for mapping assessment data to Ed-Fi API formats.


## Common Tasks

### Check for Required Columns

Columns fall into two categories:
- **Must exist in the file**: The column is referenced by an earthmover YAML operation that will error if it's missing. Whether it needs VALUES depends on the specific operation (see below).
- **Not required**: The column is either in `optional_fields` (auto-created with empty values if missing) OR only referenced in Jinja templates (Jinja2's `Undefined` class handles missing columns gracefully — `| length` returns 0, so null-checked scores are silently skipped).

**Key technical detail (verified in earthmover source code):**
Earthmover uses Jinja2 3.x's default `Undefined` class. When a column is missing from the CSV and referenced in a template:
- `Undefined is not none` → `True` (Undefined is NOT None!)
- `Undefined | length` → `0` (this is what actually filters it out)
- So the common pattern `if x is not none and x | length` correctly skips missing columns without errors.
- Columns ONLY referenced in templates with `| length` checks do NOT need to exist as headers.

Process for determining required columns:
1. Read the earthmover.yaml file. ONLY the following operations require columns to exist:
   - `duplicate_columns`: column must exist (errors with "column X not present in the dataset")
   - `combine_columns`: columns must exist (uses `raise_on_unmatched=True`)
   - `rename_columns`: column must exist (errors with "column X not present in the dataset")
   - `date_format`: column must exist (uses `raise_on_unmatched=True`)
   - `keep_columns`: column must exist (uses `raise_on_unmatched=True`)
   - `map_values`: column must exist (uses `raise_on_unmatched=True`)
   - `join` left keys: must exist (pandas merge will error)
   - `group_by`: columns must exist (pandas groupby will error on missing columns)
   - `filter_rows`: columns in query must exist (pandas query will error)
   - `expect`: columns in assertions must exist and have values
   - `POSSIBLE_STUDENT_ID_COLUMNS`: all listed columns must exist as headers; one must have values in every row
   - Columns in `optional_fields` are auto-created with `fill_value=""` if missing — they do NOT need to exist.
   - Columns ONLY referenced in Jinja templates do NOT need to exist (see technical detail above).

2. For columns that must exist, determine if they also need VALUES:
   - `duplicate_columns` / `combine_columns`: need values if used to build identifiers (e.g., studentAssessmentIdentifier)
   - `date_format`: needs a parseable date value or will error
   - `join` with `join_type: inner`: records are silently dropped if value doesn't match seed — check if blanks are handled in the seed file
   - `join` with `join_type: left`: values can be empty (unmatched rows get nulls), BUT check that the template properly null-checks joined columns — NaN values get stringified as `"nan"` and can cause 400 errors from Ed-Fi if sent as descriptor values
   - `filter_rows`: behavior depends on the query — check if empty values would cause unintended filtering
   - `rename_columns`: header must exist, but values can be empty if the template null-checks them

3. Create a required_columns.csv test file:
   - Include "must have values" columns with valid values
   - Include "must exist as header" columns WITH EMPTY VALUES to verify the bundle handles them gracefully
   - Include at least one row where optional score values are populated and one where they are empty

4. End-to-end test with edfi_testing_stack:
   - The testing stack repo is at `/home/jalvord/code/edfi_testing_stack/`
   - Install if needed: `pip install -e /home/jalvord/code/edfi_testing_stack/`
   - Some bundles use `lightbeam.yml` instead of `lightbeam.yaml`. test-bundle looks for `lightbeam.yaml`, so copy/rename the file if needed.
   - Before running, temporarily modify the bundle's lightbeam.yaml:
     - Add `namespace_overrides: {}` (lightbeam bug — crashes without it)
     - Set `verify_ssl: False` (local stack uses HTTP, not HTTPS)
     - Do NOT change `mode` — `district_specific` works with the local stack
   - Run the test-bundle command:
     ```bash
     test-bundle /path/to/bundle -p '{"OUTPUT_DIR": "./output", "STATE_FILE": "./runs.csv", "INPUT_FILE": "./data/required_columns.csv", ...}' -v -kr
     ```
     - Use `-v` for verbose output to see lightbeam details
     - Use `-kr` to keep containers running between tests
     - Pass earthmover parameters via `-p` matching the bundle's README example
   - If running a second bundle while containers are already up, spin down first (`edfi-stack down`) so the new bundle's namespace gets registered
   - The stack takes ~2 minutes to spin up — "Waiting for API to come online..." is normal
   - Success looks like: all endpoints return 201 status codes and you see the rainbow message
   - 409 errors on objectiveAssessments can indicate dependency ordering issues (not related to required_columns)
   - If it breaks, the error message will tell you what's missing — fix the required_columns.csv and re-run
   - After testing, revert the lightbeam.yaml changes (namespace_overrides and verify_ssl)

5. Document the findings:
   - List columns that must have values and explain why (assertion, used in transformation, needed for valid Ed-Fi output)
   - List columns that must exist as headers but can be empty
   - Note any data format requirements (date formats, enum values, etc.)
   - Identify silent filtering scenarios (inner joins that exclude records)

### Creating DATA_REQUIREMENTS.md Files

DATA_REQUIREMENTS.md files are **user-facing documentation for district staff** who provide source data files. These users will NOT be running the bundles themselves - they are just supplying the data that will be processed by technical staff or through Runway.

**Audience:**
- District data coordinators
- Assessment coordinators
- Non-technical staff who export files from assessment systems

**What to include:**
- List of required columns with plain-language names
- Data format requirements (with examples of valid and invalid formats)
- Clear examples of proper formatting
- What NOT to do (common mistakes with ❌ markers)

**What NOT to include:**
- Instructions on how to run earthmover commands
- References to CLI parameters (like `TEST_TYPE`, `API_YEAR`, `STUDENT_ID_NAME`)
- References to sample files in the bundle (users won't have access to the repo)
- Technical implementation details (Ed-Fi schemas, Jinja templates, earthmover operations)
- GitHub links or references to code
- Explanations of "why" things work a certain way - users just need to know what format to use

**Tone and style:**
- Write for a non-technical audience
- Use plain language, not developer jargon
- Focus on "what your data should look like" not "how the bundle processes it"
- Provide concrete examples with actual values (e.g., "10/12/2015" not "MM/DD/YYYY")
- Be direct and prescriptive - tell them exactly what format to use

**Common patterns:**
- "Must be in X format" with examples
- "Valid values are: A, B, C" for enums
- "❌ Will NOT work:" sections showing common mistakes
- Brief notes about records being excluded when values are invalid (keep it minimal)

**Example of good vs. bad phrasing:**

Bad (too technical):
> "The `TEST_TYPE` parameter must be set to `SAT` when running the bundle"

Good (user-focused):
> "Test Date must be in M/D/YYYY format (e.g., 10/12/2015)"

Bad (references files users don't have):
> "Check the sample_anonymized_file_sat.csv for examples"

Good (standalone guidance):
> "For example: `10/12/2015` for October 12, 2015"

Bad (explains implementation):
> "Ed-Fi expects numeric values for score fields"

Good (just states the requirement):
> "Scores must be numbers or left blank. Do not use dashes or text like 'N/A'."

### Reviewing bundle code:
If I ask you to review a bundle, fetch and follow the Bundle Review Checklist from Slite (doc ID: `6zJA95bkBivsg9`, URL: https://edanalytics.slite.com/app/docs/6zJA95bkBivsg9). You must confirm that you've checked and give me the results of each item in the checklist.
