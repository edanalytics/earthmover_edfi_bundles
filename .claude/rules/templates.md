# Template Engineering Best Practices

This document outlines best practices for writing .jsont templates in earthmover assessment bundles.

## Null Handling Patterns

### The Problem: Ed-Fi Rejects Empty Strings

Ed-Fi validation rules:
- Empty strings (`""`) for scores or performance levels cause validation failures
- Arrays cannot be empty if included (must have at least 1 element)
- **At least 1 performance level OR score result required per StudentAssessment**

### The Solution: Build Lists, Then Loop

**Pattern:** Build lists of non-null values at the top of your template, then loop over validated lists.

**Example from Slite documentation:**

```jinja
{# Build lists of non-null score results #}
{% set scoreResults = [] %}
{% if ${scale_score} %}
  {% set _ = scoreResults.append({
    "assessmentReportingMethodDescriptor": "${assessment_reporting_method_descriptor_namespace}AssessmentReportingMethodDescriptor#Scale Score",
    "resultDatatypeTypeDescriptor": "${DESCRIPTOR_NAMESPACE}ResultDatatypeTypeDescriptor#Integer",
    "result": "${scale_score}"
  }) %}
{% endif %}
{% if ${percentile_rank} %}
  {% set _ = scoreResults.append({
    "assessmentReportingMethodDescriptor": "${assessment_reporting_method_descriptor_namespace}AssessmentReportingMethodDescriptor#Percentile",
    "resultDatatypeTypeDescriptor": "${DESCRIPTOR_NAMESPACE}ResultDatatypeTypeDescriptor#Integer",
    "result": "${percentile_rank}"
  }) %}
{% endif %}

{# Build list of non-null performance levels #}
{% set performanceLevels = [] %}
{% if ${performance_level} %}
  {% set _ = performanceLevels.append({
    "assessmentReportingMethodDescriptor": "${assessment_reporting_method_descriptor_namespace}AssessmentReportingMethodDescriptor#Performance Level",
    "performanceLevelDescriptor": "${performance_level_descriptor_namespace}PerformanceLevelDescriptor#${performance_level}",
    "performanceLevelMet": true
  }) %}
{% endif %}

{
  "studentAssessmentIdentifier": "${student_assessment_identifier}",
  "assessmentReference": { ... },
  "studentReference": { ... },
  "administrationDate": "${administration_date}",
  "whenAssessedGradeLevelDescriptor": "${grade_level_descriptor}",

  {# Only include arrays if they have values #}
  {% if scoreResults %}
  "scoreResults": [
    {% for score in scoreResults %}
    {{ score | tojson }}{{ "," if not loop.last }}
    {% endfor %}
  ],
  {% endif %}

  {% if performanceLevels %}
  "performanceLevels": [
    {% for pl in performanceLevels %}
    {{ pl | tojson }}{{ "," if not loop.last }}
    {% endfor %}
  ]
  {% endif %}
}
```

### Key Principles

1. **Check before appending:** Use `{% if ${column} %}` to check for non-null values
2. **Build complete objects:** Append full dictionaries, not partial data
3. **Conditionally include arrays:** Only output the array if the list has elements
4. **No trailing commas:** Use `{{ "," if not loop.last }}` in loops

## Grain Matching Requirements

### Ed-Fi StudentAssessment Entity Grain

The Ed-Fi StudentAssessment entity has a unique key constraint on:
- `assessmentIdentifier`
- `namespace`
- `studentAssessmentIdentifier`
- `studentUniqueId`

**Your earthmover output grain must match this exactly.**

### Common Grain Issues

#### Problem: Multiple Rows Per Student Assessment

Some vendor files have one row per objective assessment score, creating multiple rows for the same student assessment:

```
student_id,test_date,overall_score,domain_1_score,domain_2_score
12345,2023-10-15,85,80,90
```

vs.

```
student_id,test_date,domain,score
12345,2023-10-15,domain_1,80
12345,2023-10-15,domain_2,90
```

**Solution for second format:** Group/aggregate before template, or use Renaissance STAR pattern with separate StudentAssessments.

#### Renaissance STAR Example

STAR files have one row per skill area. The bundle creates:
1. **One StudentAssessment** per domain group (Comprehension, Literacy)
2. **Separate StudentAssessments** for each skill area (as distinct assessments)

This matches the Ed-Fi grain while preserving all vendor data.

### Checking Grain Before Writing Templates

1. **Examine source data structure:** How many rows per student test event?
2. **Design studentAssessmentIdentifier:** Must be unique within grain
3. **Plan aggregation if needed:** Group in transformations before template
4. **Validate uniqueness:** Check output for duplicate keys

## Ed-Fi Validation Rules

### Required Fields

**Every StudentAssessment must have:**
- At least 1 performance level **OR** at least 1 score result
- Cannot have empty arrays for either
- Can omit the array entirely if no data

**Example of valid minimal StudentAssessment:**

```json
{
  "studentAssessmentIdentifier": "2023_Fall",
  "assessmentReference": { ... },
  "studentReference": { ... },
  "administrationDate": "2023-10-15",
  "whenAssessedGradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Third grade",
  "scoreResults": [
    {
      "assessmentReportingMethodDescriptor": "uri://example.org/AssessmentReportingMethodDescriptor#Scale Score",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer",
      "result": "450"
    }
  ]
}
```

### Empty String Rules

**Invalid:**
```json
"result": ""  // Will fail validation
```

**Valid:**
```json
// Omit the score entirely, or:
{% if ${score} %}
"result": "${score}"
{% endif %}
```

### Trailing Comma Issues

**Problem:** JSON doesn't allow trailing commas, but Jinja loops can create them.

**Solution:**
```jinja
{% for item in items %}
{{ item | tojson }}{{ "," if not loop.last }}
{% endfor %}
```

## Jinja Conditional Patterns

### Year-Based Conditionals

Use for Ed-Fi version changes or assessment changes over time:

```jinja
{% if ${API_YEAR} >= 2022 %}
  "newFieldIntroducedIn2022": "${value}",
{% endif %}
```

### Version-Based Conditionals

For Ed-Fi data model version differences:

```jinja
{% if ${EDFI_VERSION} == "5.0" %}
  "edfi5Field": "${value}",
{% elif ${EDFI_VERSION} == "3.0" %}
  "edfi3Field": "${value}",
{% endif %}
```

### When to Split Bundles vs. Use Conditionals

**Use conditionals when:**
- Minor field differences between years/versions
- Same core data structure
- Conditional logic is simple and readable

**Split into separate bundles when:**
- Major structural changes
- Different vendor file formats
- Complex conditional logic that reduces maintainability

## Template Structure Best Practices

### Organize studentAssessment.jsont

**Recommended structure:**

```jinja
{# 1. Define helper variables and lists at top #}
{% set scoreResults = [] %}
{% set performanceLevels = [] %}

{# 2. Build non-null score results #}
{% if ${scale_score} %}
  {% set _ = scoreResults.append({...}) %}
{% endif %}

{# 3. Build non-null performance levels #}
{% if ${performance_level} %}
  {% set _ = performanceLevels.append({...}) %}
{% endif %}

{# 4. Output main entity #}
{
  "studentAssessmentIdentifier": "${student_assessment_identifier}",
  "assessmentReference": {
    "assessmentIdentifier": "${assessment_identifier}",
    "namespace": "${assessment_namespace}"
  },
  "studentReference": {
    "studentUniqueId": "${edFi_studentUniqueID}"
  },
  "schoolYearTypeReference": {
    "schoolYear": ${API_YEAR}
  },
  "administrationDate": "${administration_date}",
  "whenAssessedGradeLevelDescriptor": "${grade_level_descriptor}",

  {# 5. Conditionally include arrays #}
  {% if scoreResults %}
  "scoreResults": [
    {% for score in scoreResults %}
    {{ score | tojson }}{{ "," if not loop.last }}
    {% endfor %}
  ],
  {% endif %}

  {% if performanceLevels %}
  "performanceLevels": [
    {% for pl in performanceLevels %}
    {{ pl | tojson }}{{ "," if not loop.last }}
    {% endfor %}
  ],
  {% endif %}

  "studentAssessmentEducationOrganizationAssociation": {
    "educationOrganizationAssociationTypeDescriptor": "uri://ed-fi.org/EducationOrganizationAssociationTypeDescriptor#School",
    "educationOrganizationReference": {
      "educationOrganizationId": ${edFi_schoolID}
    }
  }
}
```

### Reusable Patterns for Objective Assessments

Similar null handling applies to objective assessment scores:

```jinja
{% set objectiveScores = [] %}
{% if ${objective_1_score} %}
  {% set _ = objectiveScores.append({
    "assessmentReportingMethodDescriptor": "...",
    "resultDatatypeTypeDescriptor": "...",
    "result": "${objective_1_score}"
  }) %}
{% endif %}

{% if objectiveScores %}
"studentObjectiveAssessments": [
  {
    "objectiveAssessmentReference": { ... },
    "scoreResults": [
      {% for score in objectiveScores %}
      {{ score | tojson }}{{ "," if not loop.last }}
      {% endfor %}
    ]
  }
]
{% endif %}
```

## Common Template Mistakes

### ❌ Looping Without Null Checks

**Wrong:**
```jinja
"scoreResults": [
  {
    "result": "${scale_score}"
  },
  {
    "result": "${percentile}"
  }
]
```

**Why:** If either score is null, creates empty string that fails validation.

**Correct:** Use the build-list-then-loop pattern shown above.

### ❌ Incorrect Grain in Transformations

**Wrong:** Outputting one row per objective assessment when source has one row per student test.

**Correct:** Match transformation output to Ed-Fi entity grain (one StudentAssessment per student test event).

### ❌ Hard-Coded Descriptor Namespaces

**Wrong:**
```jinja
"resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer"
```

**Correct:**
```jinja
"resultDatatypeTypeDescriptor": "${DESCRIPTOR_NAMESPACE}ResultDatatypeTypeDescriptor#Integer"
```

### ❌ Using Empty Strings Instead of Omitting

**Wrong:**
```jinja
"result": "{{ ${score} or '' }}"
```

**Correct:**
```jinja
{% if ${score} %}
"result": "${score}"
{% endif %}
```

## Testing Templates

### Validate JSON Structure

After running earthmover:
```bash
jq . output/studentAssessments.jsonl
```

Should return valid JSON. Check for:
- No trailing commas
- No empty strings in scores/performance levels
- At least 1 score or performance level per record

### Check for Empty Arrays

```bash
cat output/studentAssessments.jsonl | jq 'select(.scoreResults == [])'
```

Should return no results (empty arrays should be omitted, not included).

### Verify Grain

```bash
cat output/studentAssessments.jsonl | jq -r '[.assessmentReference.assessmentIdentifier, .studentAssessmentIdentifier, .studentReference.studentUniqueId] | @csv' | sort | uniq -d
```

Should return no duplicates (no rows mean no duplicates, which is correct).

## References

- **Slite Documentation:** "Writing earthmover bundles" (template section)
- **Ed-Fi Validation Rules:** https://edfi.atlassian.net/wiki/spaces/ODSAPIS3V53/pages/22487121/StudentAssessment
- **Existing Bundle Templates:** See `assessments/*/templates/` directories for examples
- **Earthmover Jinja Documentation:** https://github.com/edanalytics/earthmover
