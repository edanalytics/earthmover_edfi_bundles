# Bundle Quality Checklist

This comprehensive checklist should be used when reviewing or creating assessment bundles. All items must be validated before opening a PR.

## Governance Checks

### ✓ Assessment Identifiers
- [ ] Follow `{Title} {Subject}` pattern
- [ ] Highest level at which scores exist (typically subject-level)
- [ ] **NO vendor name in identifier** (captured by namespace)
- [ ] Include `assessmentFamily` for cross-subject grouping
- [ ] Use "Composite" or "Overall" for cross-subject assessments
- [ ] Consistent with existing bundles for same vendor

### ✓ Namespaces
- [ ] Use vendor's actual domain: `uri://{vendor-domain}/{assessment-name}/`
- [ ] Assessment-specific descriptors use vendor namespace
- [ ] Non-assessment-specific descriptors use Ed-Fi namespace (`uri://ed-fi.org`)
- [ ] `resultDatatypeTypeDescriptor` uses `${DESCRIPTOR_NAMESPACE}` parameter

### ✓ Assessment Hierarchy
- [ ] Captures true assessment structure from vendor
- [ ] Objective assessments for subscores/domains/reporting categories
- [ ] Parent objective assessments for nested hierarchies (if applicable)
- [ ] Hierarchy matches vendor documentation and sample data

### ✓ studentAssessmentIdentifier
- [ ] Unique within context of student + assessment + school year
- [ ] Appropriate concatenation or vendor-provided ID
- [ ] Tested for uniqueness in sample data output

## Descriptor Checks

### ✓ Assessment-Specific Descriptors (Vendor Namespace)
- [ ] `assessmentReportingMethodDescriptor`: vendor namespace, original codeValue
- [ ] `performanceLevelDescriptor`: vendor namespace, original codeValue
- [ ] `assessmentPeriodDescriptor`: vendor namespace (if used)
- [ ] `assessmentCategoryDescriptor`: vendor namespace (if used)
- [ ] Seed files created in `seeds/` directory for custom descriptors

### ✓ Non-Assessment-Specific Descriptors (Ed-Fi Namespace)
- [ ] `gradeLevelDescriptor`: uses `uri://ed-fi.org` namespace
- [ ] `academicSubjectDescriptor`: uses `uri://ed-fi.org` namespace
- [ ] Standard Ed-Fi codeValues used (e.g., "Third grade", not "3rd grade")

### ✓ No Hard-Coded Namespaces
- [ ] `resultDatatypeTypeDescriptor` uses `${DESCRIPTOR_NAMESPACE}` parameter
- [ ] No `uri://ed-fi.org` hard-coded in templates
- [ ] All descriptor namespaces properly parameterized or from source data

### ✓ Score Preservation
- [ ] Original score names preserved (e.g., "RIT Scale Score", not "Scale Score")
- [ ] Vendor-specific calculation methodologies maintained
- [ ] No normalization at integration layer

## Technical Checks

### ✓ Data Mapping
- [ ] All possible scores from vendor mapped
- [ ] All performance levels mapped
- [ ] Objective assessment scores mapped (if applicable)
- [ ] No data loss between source and output

### ✓ Null Handling
- [ ] No empty strings (`""`) sent for scores or performance levels
- [ ] Build-list-then-loop pattern used in templates
- [ ] Conditional array inclusion (only if list has elements)
- [ ] At least 1 performance level OR score result per StudentAssessment

### ✓ Grain Matching
- [ ] Output grain matches Ed-Fi StudentAssessment entity:
  - `assessmentIdentifier`
  - `namespace`
  - `studentAssessmentIdentifier`
  - `studentUniqueId`
- [ ] No duplicate StudentAssessment records in output
- [ ] Aggregation/grouping applied if source grain differs

### ✓ Grade Level Mapping
- [ ] Tested grade in `whenAssessedGradeLevelDescriptor` (grade when assessed)
- [ ] NOT current grade or enrolled grade
- [ ] Proper Ed-Fi codeValue format (e.g., "Third grade")

### ✓ Education Organization Association
- [ ] Uses `studentAssessmentEducationOrganizationAssociation`
- [ ] `associationTypeDescriptor` set (typically "School")
- [ ] `educationOrganizationReference` points to testing location

### ✓ Date Fields
- [ ] `administrationDate` in ISO format (YYYY-MM-DD)
- [ ] `schoolYearTypeReference` properly set (typically `${API_YEAR}`)
- [ ] Time components handled if present in source data

## Template Checks

### ✓ JSON Validity
- [ ] Valid JSON structure (no syntax errors)
- [ ] No trailing commas in objects or arrays
- [ ] Proper quote escaping in string values
- [ ] Descriptor values in correct format: `namespace#codeValue`

### ✓ Conditional Logic
- [ ] Year-based conditionals for version changes (if applicable)
- [ ] Proper Jinja syntax (`{% if %}`, `{% endif %}`)
- [ ] Comma handling in loops: `{{ "," if not loop.last }}`
- [ ] Logic is readable and maintainable

### ✓ Objective Assessments
- [ ] Properly nested in `studentObjectiveAssessments` array
- [ ] `objectiveAssessmentReference` points to correct assessment
- [ ] Score/performance level handling same as parent (null checks)
- [ ] Hierarchy matches Assessment/ObjectiveAssessment relationships

## Student ID Xwalking Compatibility

### ✓ Package Integration Support
- [ ] Empty initial transformation node (no filtering/aggregation)
- [ ] `STUDENT_ID_NAME` parameter with default `edFi_studentUniqueID`
- [ ] Column reference: `${edFi_studentUniqueID}` in templates
- [ ] Compatible with `packages/student_ids/` structure

### ✓ Parameter Usage
- [ ] Default allows standard usage (vendor ID = Ed-Fi ID)
- [ ] Supports xwalking when needed (joins happen in packages)
- [ ] Documentation mentions xwalking option

## Data Quality Checks

### ✓ Sample Anonymized File
- [ ] Included in `data/` directory
- [ ] Matches vendor's standard file structure
- [ ] Covers all score types and performance levels
- [ ] Includes objective assessment data (if applicable)

### ✓ No PII in Sample Data
- [ ] No student names
- [ ] No real student IDs (use synthetic: 9999...)
- [ ] No real district/school identifiers
- [ ] No teacher names or staff identifiers
- [ ] Dates adjusted if needed (use recent but generic dates)
- [ ] Sample file generated using proper anonymization workflow
- [ ] Original sample files with PII were NEVER copied/moved into repository

See `.claude/rules/sample-data-handling.md` for complete anonymization procedures.

### ✓ Data Coverage
- [ ] Multiple grade levels represented
- [ ] Multiple test administrations (if applicable)
- [ ] Range of scores (low, medium, high)
- [ ] All performance levels represented
- [ ] Edge cases covered (missing scores, missing performance levels)

## Configuration Checks

### ✓ earthmover.yaml
- [ ] Single file per bundle (use composition if multiple configs needed)
- [ ] Parameter defaults defined
- [ ] Relative paths only (no BUNDLE_DIR variable)
- [ ] Proper source file type specified
- [ ] Transformations follow best practices (rename/modify, then template)

### ✓ lightbeam.yaml
- [ ] Single file per bundle
- [ ] Selector matches earthmover output
- [ ] Proper endpoint order (POST before PUT/DELETE)
- [ ] Year-based selectors if API year affects output

### ✓ bundle_metadata.json
- [ ] All parameters documented
- [ ] Required vs. optional clearly marked
- [ ] Default values match earthmover.yaml
- [ ] Field requirements section lists source columns
- [ ] Description clear and accurate

### ✓ _metadata.yaml
- [ ] Assessment name matches identifier
- [ ] Namespace URI correct
- [ ] Grade levels array complete
- [ ] Subjects array correct
- [ ] Description is clear and concise
- [ ] Tags appropriate

## Documentation Checks

### ✓ README.md
- [ ] Working example command included
- [ ] Parameter descriptions match bundle_metadata.json
- [ ] Output description accurate
- [ ] Links to vendor documentation (if public)
- [ ] Special considerations documented (if any)

### ✓ Seed File Documentation
- [ ] All custom descriptors in seeds/ directory
- [ ] CSV format correct (descriptor, codeValue, shortDescription, description, namespace)
- [ ] Values match template usage exactly
- [ ] Descriptions are clear and vendor-specific

### ✓ Code Comments
- [ ] Earthmover config has comments for non-obvious logic
- [ ] Templates have comments for complex conditionals
- [ ] Transformation steps are clear

## Testing Checks

### ✓ Earthmover Validation
- [ ] `earthmover run` completes without errors
- [ ] Output files created in `output/` directory
- [ ] JSONL files are valid (can be parsed by jq)
- [ ] No error messages in earthmover log
- [ ] State file tracking works correctly

### ✓ test-bundle Command
- [ ] Run from [edfi_testing_stack](https://github.com/edanalytics/edfi_testing_stack)
- [ ] All student assessments POST successfully
- [ ] No validation errors from Ed-Fi ODS
- [ ] Check Ed-Fi logs for warnings
- [ ] Verify data appears correctly in ODS

### ✓ Output Validation
- [ ] No empty strings in scores/performance levels
- [ ] No empty arrays included
- [ ] At least 1 score OR performance level per record
- [ ] No duplicate StudentAssessment records
- [ ] Descriptor values are valid (namespace#codeValue format)

### ✓ Manual Verification
- [ ] Spot-check output records against source data
- [ ] Verify score values match
- [ ] Verify performance levels match
- [ ] Check objective assessment nesting
- [ ] Confirm grade levels are correct

## Registry Synchronization

### ✓ Registry Generation
- [ ] Run `python create-registry.py assessments --output registry.json`
- [ ] Commit updated `registry.json` with bundle changes
- [ ] Verify bundle appears in registry with correct metadata
- [ ] CI will fail if registry is out of sync

## Version Control

### ✓ Git Checks
- [ ] Branch from `main`
- [ ] Meaningful commit messages
- [ ] No unnecessary files committed (no `output/`, `__pycache__`, etc.)
- [ ] `.gitignore` properly excludes generated files
- [ ] PR title clearly describes bundle addition/change

### ✓ PR Description
- [ ] Assessment vendor and name
- [ ] Governance artifact link (if new bundle)
- [ ] Testing results summary
- [ ] Any special considerations
- [ ] Screenshots of successful load (optional but helpful)

## Final Verification Steps

Before opening PR:

1. **Run quality checks:**
   ```bash
   # Lint Python
   ruff check .
   ruff format .

   # Lint YAML
   yamllint .

   # Validate with earthmover
   cd assessments/<BUNDLE_NAME>
   earthmover run -c earthmover.yaml -p '{"INPUT_FILE": "data/sample.csv", "API_YEAR": 2024}'

   # Validate JSON output
   jq . output/studentAssessments.jsonl > /dev/null
   ```

2. **Test with Ed-Fi ODS:**
   ```bash
   # From edfi_testing_stack
   test-bundle --bundle <BUNDLE_NAME> --input data/sample.csv --year 2024
   ```

3. **Update registry:**
   ```bash
   python create-registry.py assessments --output registry.json
   ```

4. **Review this checklist:** Confirm all items are checked

## References

- **Full Slite Checklist:** "Bundle Review Checklist"
- **Bundle Development Workflow:** "Writing earthmover bundles" (12-step process)
- **Governance Standards:** See `.claude/rules/governance.md`
- **Descriptor Rules:** See `.claude/rules/descriptors.md`
- **Template Best Practices:** See `.claude/rules/templates.md`
