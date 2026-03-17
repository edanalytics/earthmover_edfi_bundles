# Claude Code Instructions for earthmover_edfi_bundles

This file contains project-specific instructions and preferences for Claude Code when working in this repository.

## Project Overview
This repository contains earthmover bundles for mapping assessment data to Ed-Fi API formats.


## Common Tasks

### Check for Required Columns

Columns fall into three categories:
- **Must have values**: The column must exist AND contain data. Missing values would break the earthmover run or produce invalid Ed-Fi output (e.g., empty `scoreResults` array).
- **Must exist as header (values can be empty)**: The column header must be present in the file (because it's in `rename_columns` and NOT in `optional_fields`), but the template null-checks the values so empty cells are handled gracefully.
- **Optional**: The column is listed in `optional_fields`, so neither the header nor values need to exist.

Process for determining required columns:
1. Read the earthmover.yaml file to identify:
   - Columns in `duplicate_columns` operations (must have values)
   - Columns in `combine_columns` operations (must have values)
   - Columns with `expect` assertions (must have values)
   - Columns used in `modify_columns` for transformations like date parsing (must have values)
   - Columns used in `join` operations with `join_type: inner` (records filtered if missing/invalid - check if blanks are handled in the seed)
   - Columns in `rename_columns` that are NOT in `optional_fields` (must exist as headers - but check step 2 to determine if values are also needed)
   - Columns referenced in `filter_rows` operations (must have values for filtering logic)

2. Read the template files to determine which "header required" columns also need values:
   - Variables referenced directly without null checks → must have values
   - Variables in null-checked loops (e.g., `if score[0] is not none and score[0] | length`) → values can be empty
   - Pay special attention to Ed-Fi required arrays like `scoreResults` - at least one item must pass null checks or the output is invalid

3. Create a required_columns.csv test file:
   - Include "must have values" columns with valid values
   - Include "must exist as header" columns WITH EMPTY VALUES to verify the bundle handles them gracefully
   - Include at least one row where optional score values are populated and one where they are empty

4. Run earthmover with the required_columns.csv:
   - Use the example command from the bundle's README
   - Point INPUT_FILE to the required_columns.csv
   - Use the bundle's default output directory (./output) and runs file (./runs.csv)
   - Do NOT create separate test output directories or runs files
   - If it breaks, the error message will tell you what's missing
   - If it succeeds, proceed to step 5

5. Check the output:
   - Validate the output JSONL files contain all expected required fields per Ed-Fi schema
   - Check for null values or empty strings in required fields
   - Verify records weren't silently filtered out due to inner joins with invalid data
   - For rows with empty "header only" columns, verify the output still has valid `scoreResults` (not an empty array)

6. Document the findings:
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
If I ask you to review a bundle, you must confirm that you've checked and give me the results of each of the below instructions:

- Check assessment identifiers/objective assessment identifiers & namespaces
  - Ensure identifiers are following governance rules.
  - TLDR:
    - Capture true hierarchy of the assessment using assessment/objective assessment IDs.
    - Assessment ID should be the highest level at which scores are captured.
      - Often times captured at the subject level, sometimes composite, sometimes something totally different (like form level for MAP Fluency).
      - Title + subject (unless single subject) is a decent rule to follow as a starting point.
    - Do not include vendor in the ID.
  - Namespaces should link to the underlying vendor of that assessment.
  - Ensure an assessment family is included in the data model.
- Check studentAssessmentIdentifier to ensure it acurately captures a unique student assessment record
  - If the assessment file already contains a unique identifier for a student record, use that as the studentAssessmentIdentifier .
    - Otherwise, ensure the combination of columns used to create one does result in a unique ID.
      - Ideally using documentation and not an a single sample file
- Check descriptors & namespaces
  - General guidance:
    - For assessment-specific descriptors (this includes but isn't limited to assessmentPeriods, assessmentReportingMethods, performanceLevel): the namespace should link to the underlying vendor of that assessment (e.x. renaissance for STAR, collegeboard for PSAT/SAT, etc). The codeValue should match the original values (whether that be score names, periods, etc) from the vendor file.
      - These descriptors will be sent to the ODS with the studentAssessment/assessment/objectiveAssessment results.
    - For non-assessment-specific descriptors (this includes but isn't limited to gradeLevels, academicSubjects, etc. - essentially any descriptors that are also used by resources other than assessment-related resources): the namespace/code values should almost always be the default Ed-Fi namespace/codeValues.
      - The ONLY time when this may not be true is if the assessment is STRICTLY administered in a specific local context, aka is a state-specific assessment
      - Ensure these default values are reasonable.
    - NO descriptors namespaces should be hard-coded in any template because it is then harder to override
      - resultDataTypeDescriptor namespaces should be filled in via a parameter: DESCRIPTOR_NAMESPACE - this parameter should not be used otherwise - see this as an example of this param.
  - Make sure things like subjects seem reasonable as defaults
  - Also check namespaces
- Check that all possible scores are mapped
  - The general guidance is that we should send as much information from the source file as possible into Ed-Fi given the wide range of analytic use-cases for assessment data.
  - We generally do not send student demographics as there is no spot in the Ed-Fi model for them and sending them as score results is not best practice.
- Check for anything that could be considered invalid json
  - Trailing commas, etc.
  - Ensure descriptor values are in proper json format (not just list of strings).
- Check to ensure that we are properly handling missing values/not sending empty strings
  - Ed-Fi will not accept an empty string.
  - All score/PLs should be contained in a list and looped over to ensure they are not null.
    - This should happen at the top of the studentAssessment.jsont file so that we can easily update if necessary.
      - ^ true for scores, performance levels, and objective assessments/corresponding scores/PLs.
```#this should be done at the top of the studentAssessment.jsont file
"scoreResults": [
    {%- set possible_scores = [
        [scaleScore, "Scale Score", "Integer"],
        [sem, "SEM", "Integer"]
    ] -%}

    {%- set scores = [] -%}
    {%- for score in possible_scores -%}
      {%- if score[0] is not none and score[0] | length -%}
        {%- set _ = scores.append(score) -%}
      {%- endif -%}
    {%- endfor -%}

#this part must be part of the actual template
    {% for score in scores %}
      {
        "assessmentReportingMethodDescriptor": "{{namespace}}/AssessmentReportingMethodDescriptor#{{score[1]}}",
        "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#{{score[2]}}",
        "result": "{{score[0]}}"
      } {% if not loop.last %},{% endif %}
    {% endfor %}
  ]```
- Check that the student ID package would be compatible
  - Empty initial transformation node
  ``transformations:
    input:
      source: $sources.input
      operations: []```
  - Parameter defaults
    - STUDENT_ID_NAME
      - Should default to 'edFi_studentUniqueID', which is the column added by the apply_xwalk package of student ID xwalking feature.
- Check logic to transform the files, especially if they are wide
  - Goal is to ensure we won't unintentionally run into memory issues, performance issues, etc.
- Check grade level mapping
  - The general guidance is to go against the definition of whenAssessedGradeLevel by including the tested grade in that property (instead of the enrolled grade, which is what the definition suggests. Tested grade does not necessarily = enrolled grade).
    - Reasoning behind this: tested grade is typically more useful analytically, and enrolled grade can be found in the studentEducationOrganizationAssociation resource anyway.
  - If both tested and enrolled grades exist in the underlying assessment data, send the enrolled grade as a separate scoreResult.
- Check for correct usage of the studentAssessmentEducationOrganizationAssociation resource
  - Ensure that the associationType is correct based on the documentation of the assessment.
  - We prefer using this resource instead of the reportedSchoolAssociation property of the studentAssessment resource because this resource includes the associationType property.
- Check for xwalk values that could change yearly, ask for the writer to check if static
  - (if they do change and we don't realize, we would have to reload data, which wouldn't be fun).
    - This includes but is not limited to: performance levels based on thresholds, labels, etc. Example here of a confirmed static xwalk.
    - Ideally, our bundles do little mappings in general because districts will want to see the original values, and additional mapping for viz can occur downstream.
- If a Runway assessment: ensure compatibility with Runway
  - Non-assessment specific descriptors (aka those with Ed-Fi namespace defaults) must be in their own file that is named for the descriptor type. E.g. gradeLevelDescriptors.csv
    - The actual descriptor column must be named edfi_descriptor
  - A _metadata.yaml file must be created
- Do not inner join seeds/mappings for fields that are not required
  - For example, do not inner join grade mappings because whenAssessedGradeLevel is not a required field
    - Instead, left join and ensure proper null handling in the template.
- Check that a sample anonymized file is included in the bundle
  - Easier testing when this exists.
  - Find real file, subset to ~5 rows, and remove ALL PII.
    - district/school/staff/student names & IDs.
      - district/school so we don't know the original source of the file.
  - ENSURE ANONYMIZED.
- Check that a single earthmover.yaml and lightbeam.yaml file exist in the bundle
- If multiple earthmover config files exist for a particular bundle, add a single file called earthmover.yaml that uses composition to combine, with proper parameterization. See here for an example.
- Check that the .README is consistent with other bundles and includes an example command that can be successfully run against the sample file
