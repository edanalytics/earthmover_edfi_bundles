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

4. When running earthmover manually (outside of test-bundle), always use the bundle's own `./output` directory as OUTPUT_DIR. Never use `/tmp` or other external directories.

5. End-to-end test with edfi_testing_stack:
   - The testing stack repo is at `/home/jalvord/code/edfi_testing_stack/`
   - Install if needed: `pip install -e /home/jalvord/code/edfi_testing_stack/`
   - Some bundles use `lightbeam.yml` instead of `lightbeam.yaml`. test-bundle looks for `lightbeam.yaml`, so copy/rename the file if needed.
   - Before running, temporarily modify the bundle's lightbeam.yaml:
     - Add `namespace_overrides: {}` at the **top level** of the file (NOT nested under `connection` or `edfi_api`). Lightbeam crashes without this key.
     - Set `verify_ssl: False` (under `connection`)
     - Do NOT change `mode` — `district_specific` works with the local stack
   - Run the test-bundle command using the **sample anonymized file first** (not required_columns.csv):
     ```bash
     test-bundle /path/to/bundle -p '{"OUTPUT_DIR": "./output", "STATE_FILE": "./runs.csv", "INPUT_FILE": "./data/sample_anonymized_file.csv", ...}' -v -kr
     ```
     - Use `-v` for verbose output to see lightbeam details
     - Use `-kr` to keep containers running between tests
     - Pass earthmover parameters via `-p` matching the bundle's README example
   - If running a second bundle while containers are already up, spin down first (`edfi-stack down`) so the new bundle's namespace gets registered
   - The stack takes ~2 minutes to spin up — "Waiting for API to come online..." is normal
   - Success looks like: all endpoints return 201 status codes
   - 409 errors on objectiveAssessments are a known dependency ordering issue (children sent before parents) — ignore these and do NOT retry or investigate further. StudentAssessment 409s that cascade from OA ordering issues can also be ignored.
   - 409 errors on descriptor endpoints (e.g., performanceLevelDescriptors, assessmentCategoryDescriptors) mean duplicate payloads are being sent. This is NOT expected and should be fixed. When descriptor seeds contain per-assessment rows (with an `assessmentIdentifier` column), the descriptor destination must use a deduped transformation (with `keep_columns` to drop `assessmentIdentifier` + `distinct_rows`) instead of sourcing the raw seed directly. Only the unique descriptor values should be sent.
   - If it breaks, the error message will tell you what's missing
   - Do NOT separately validate JSON output or retry individual endpoint sends if the test stack otherwise works
   - After testing, revert the lightbeam.yaml changes (namespace_overrides and verify_ssl)

6. Document the findings:
   - List columns that must have values and explain why (assertion, used in transformation, needed for valid Ed-Fi output)
   - List columns that must exist as headers but can be empty
   - Note any data format requirements (date formats, enum values, etc.)
   - Identify silent filtering scenarios (inner joins that exclude records)

### Fixing Bundles to Only Require Ed-Fi Required Columns

Bundles should only make columns required if they map to Ed-Fi required fields (plus at least one overall score). All other columns should be in `optional_fields` and handled gracefully when missing.

**Identifying what's truly required by Ed-Fi for a studentAssessment:**
- `studentAssessmentIdentifier` (required)
- `assessmentReference`: assessmentIdentifier + namespace (typically hardcoded/added by the bundle)
- `studentReference`: studentUniqueId (required — from STUDENT_ID_NAME / POSSIBLE_STUDENT_ID_COLUMNS)
- `administrationDate` (required — typically from a date column like TestDate)
- At least one `scoreResult` (required — the bundle must ensure at least one score is always present)
- Any columns needed to derive the above (e.g., TestAdmin for schoolYear calculation)

**Everything else is optional** — scores, performance levels, grade levels, platformType, objective assessments, etc. These should not cause the bundle to fail if missing.

**How to fix a bundle:**

1. **Move non-required columns to `optional_fields`** in the source definition. This auto-creates them with empty string if missing from the CSV. This is needed for columns referenced by operations that require existence (`map_values`, `filter_rows`, `join` keys, etc.).

2. **Handle NaN from left joins on optional columns.** When an optional column is used as a left join key and the value is empty, the join won't match and joined columns get pandas NaN. NaN gets stringified as `"nan"` in templates and passes `is not none and | length` checks (length of "nan" is 3). Fix by adding a `modify_columns` after the join:
   ```yaml
   - operation: modify_columns
     columns:
       edfi_descriptor: "{%raw%}{%- if value != value -%}{%- else -%}{{value}}{%- endif -%}{%endraw%}"
   ```
   The `value != value` pattern detects NaN (NaN is the only value where self-inequality is true).

3. **Verify `map_values` on optional columns works.** When a column is in `optional_fields` and missing from the CSV, all rows get empty string. `map_values` leaves unmatched values as-is, so empty strings pass through unchanged. Template null-checks (`is not none and | length`) then filter them out.

4. **Update `required_columns.csv`** to contain ONLY the truly required columns plus one score. Do NOT include optional column headers — the point is to test that the bundle runs with a minimal file.

5. **Test with BOTH files using `test-bundle`:**
   - First, spin down any running stack: `edfi-stack down`
   - Temporarily modify lightbeam.yaml: add `namespace_overrides: {}` at the **top level** and set `verify_ssl: False` under `connection`
   - **Test 1: sample_anonymized_file.csv** — verifies the bundle still works with the full file (no regressions)
     ```bash
     test-bundle /path/to/bundle -p '{"INPUT_FILE": "./data/sample_anonymized_file.csv", ...}' -v -kr
     ```
   - **Test 2: required_columns.csv** — verifies the bundle handles missing optional columns
     ```bash
     test-bundle /path/to/bundle -p '{...}' -v -kr
     ```
   - Both must produce all 201s (409 errors on objectiveAssessments from ordering issues can be ignored)
   - After testing, revert lightbeam.yaml changes

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

**Reading bundle files:** Bundle structures are predictable. Don't use an Explore agent to discover files — just read everything directly in parallel using Read calls:
- Config files: `earthmover.yaml`, `lightbeam.yaml`, `_metadata.yaml`, `README.md`, `DATA_REQUIREMENTS.md`
- All templates: `templates/*.jsont` (use Glob first if unsure of names)
- All seeds: `seeds/*.csv`
- Data files: `data/required_columns.csv`, `data/sample_anonymized_file*.csv`

**Extraneous required columns check:** When you reach the checklist items about required columns and extraneous columns, follow the full "Check for Required Columns" process documented above in this file. Trace through every operation in the earthmover.yaml to identify which columns must exist and whether each is actually needed for Ed-Fi output. Flag any columns that are made required by operations (e.g., `rename_columns`, `keep_columns`, `filter_rows`) but are never used in a template or transformation output.

**Known patterns that are NOT issues — do not flag these:**
- `STUDENT_ID_NAME` differs between the README example and the earthmover.yaml default. The README example must use a column that exists in the sample file (e.g., `StateID`), while the earthmover.yaml defaults to `edFi_studentUniqueID` for use with the student ID xwalk package. This is intentional across all bundles.
