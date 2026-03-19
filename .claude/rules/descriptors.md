# Descriptor Namespace Rules

This document outlines the rules for using descriptor namespaces in earthmover assessment bundles.

## Core Namespace Rules

### Assessment-Specific Descriptors: Use Vendor Namespace

Descriptors that are specific to the assessment vendor should use the **vendor's namespace** and preserve original codeValues.

**Assessment-specific descriptor types:**
- `assessmentPeriodDescriptor`
- `assessmentReportingMethodDescriptor`
- `performanceLevelDescriptor`
- `assessmentCategoryDescriptor`

**Rationale:** These descriptors capture vendor-specific methodologies and reporting structures. Changing the namespace or codeValue would lose semantic meaning.

### Non-Assessment-Specific Descriptors: Use Ed-Fi Default

Descriptors that are general educational concepts should use the **Ed-Fi default namespace** (`uri://ed-fi.org`).

**Non-assessment-specific descriptor types:**
- `gradeLevelDescriptor`
- `academicSubjectDescriptor`
- `resultDatatypeTypeDescriptor` (use `${DESCRIPTOR_NAMESPACE}` parameter)

**Exception:** State-specific assessments may use state namespace for certain descriptors.

## Score Preservation Philosophy

### Why EA Doesn't Normalize Scores at Integration

Education Analytics preserves vendor-specific score methodologies rather than normalizing at the integration layer.

**Key reasons:**
1. **Vendor methodologies differ fundamentally:**
   - NWEA uses "RIT Scale Score" (equal-interval scale)
   - ACT uses "Composite Score" (averaged scale)
   - DIBELS uses "Composite Score" (different from ACT)
   - Each has unique psychometric properties

2. **Semantic meaning matters:**
   - "RIT Scale Score" ≠ "Composite Score" ≠ "Scale Score"
   - Downstream analytics need to know the methodology
   - Normalization happens in dbt where context exists

3. **Custom descriptors preserve fidelity:**
   - `uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#RIT Scale Score`
   - `uri://act.org/act/AssessmentReportingMethodDescriptor#Composite Score`
   - Original codeValue preserved, namespace provides context

## DESCRIPTOR_NAMESPACE Parameter

The `DESCRIPTOR_NAMESPACE` parameter is used **only** for `resultDatatypeTypeDescriptor` values.

**Default:** `uri://ed-fi.org`

**Usage in templates:**
```jinja
{
  "resultDatatypeTypeDescriptor": "${DESCRIPTOR_NAMESPACE}ResultDatatypeTypeDescriptor#Integer"
}
```

**IMPORTANT:** Never hard-code the namespace in templates—always use the parameter.

**Common values:**
- `Integer`
- `Decimal`
- `Percentage`
- `Level` (for performance levels)

## Practical Examples

### NWEA MAP Growth

**Assessment-specific (vendor namespace):**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#RIT Scale Score",
  "performanceLevelDescriptor": "uri://www.nwea.org/map/PerformanceLevelDescriptor#Low Average"
}
```

**Non-assessment-specific (Ed-Fi namespace):**
```jinja
{
  "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Third grade",
  "academicSubjectDescriptor": "uri://ed-fi.org/AcademicSubjectDescriptor#Mathematics"
}
```

### Renaissance STAR

**Assessment-specific (vendor namespace):**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://renaissance.com/star/AssessmentReportingMethodDescriptor#Scaled Score",
  "performanceLevelDescriptor": "uri://renaissance.com/star/PerformanceLevelDescriptor#At/Above Benchmark"
}
```

### DIBELS

**Assessment-specific (vendor namespace):**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://dibels.uoregon.edu/assessment/dibels/AssessmentReportingMethodDescriptor#Composite Score",
  "performanceLevelDescriptor": "uri://dibels.uoregon.edu/assessment/dibels/PerformanceLevelDescriptor#Core Support"
}
```

**Note:** DIBELS "Composite Score" is different from ACT "Composite Score"—the namespace disambiguates.

### ACT

**Assessment-specific (vendor namespace):**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://act.org/act/AssessmentReportingMethodDescriptor#Composite Score",
  "performanceLevelDescriptor": "uri://act.org/act/PerformanceLevelDescriptor#Meeting Benchmark"
}
```

### Grade Levels (Always Ed-Fi)

```jinja
{
  "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Tenth grade"
}
```

### Academic Subjects (Always Ed-Fi)

```jinja
{
  "academicSubjectDescriptor": "uri://ed-fi.org/AcademicSubjectDescriptor#English Language Arts"
}
```

## Complete Descriptor Namespace Decision Tree

```
Is this descriptor assessment-specific?
├─ YES (assessmentReportingMethod, performanceLevel, assessmentPeriod, assessmentCategory)
│   └─ Use vendor namespace: uri://{vendor-domain}/{assessment}/
│       └─ Preserve original codeValue from vendor
│
└─ NO (gradeLevel, academicSubject, resultDatatypeType)
    └─ Use Ed-Fi default namespace: uri://ed-fi.org
        └─ Use standard Ed-Fi codeValue
```

## Common Mistakes to Avoid

### ❌ Hard-coding Descriptor Namespaces

**Wrong:**
```jinja
{
  "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer"
}
```

**Correct:**
```jinja
{
  "resultDatatypeTypeDescriptor": "${DESCRIPTOR_NAMESPACE}ResultDatatypeTypeDescriptor#Integer"
}
```

### ❌ Using Ed-Fi Namespace for Vendor-Specific Scores

**Wrong:**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://ed-fi.org/AssessmentReportingMethodDescriptor#Scale score"
}
```

**Correct:**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#RIT Scale Score"
}
```

### ❌ Using Vendor Namespace for Grade Levels

**Wrong:**
```jinja
{
  "gradeLevelDescriptor": "uri://www.nwea.org/map/GradeLevelDescriptor#Third grade"
}
```

**Correct:**
```jinja
{
  "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Third grade"
}
```

### ❌ Normalizing Score Names

**Wrong:**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#Scale Score"
}
```

**Correct:**
```jinja
{
  "assessmentReportingMethodDescriptor": "uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#RIT Scale Score"
}
```

## Seed File Generation

Assessment-specific descriptors require seed files in the `seeds/` directory:

**Example file structure:**
```
seeds/
├─ assessmentReportingMethodDescriptors.csv
├─ performanceLevelDescriptors.csv
└─ assessmentCategoryDescriptors.csv
```

**CSV format:**
```csv
descriptor,codeValue,shortDescription,description,namespace
AssessmentReportingMethodDescriptor,RIT Scale Score,RIT Scale Score,NWEA RIT Scale Score,uri://www.nwea.org/map/
```

## References

- **Slite Documentation:** "Bundle Review Checklist" (descriptor section)
- **Ed-Fi Descriptor Documentation:** https://edfi.atlassian.net/wiki/spaces/ETKB/pages/20875455/Descriptors
- **Existing Bundle Seed Files:** See `assessments/*/seeds/` directories for examples
