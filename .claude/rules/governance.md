# Assessment Bundle Governance

This document outlines the standards for assessment identifiers, namespaces, and hierarchy structures in earthmover bundles.

## Assessment Identifier Rules

### Core Structure: Title + Subject

Assessment identifiers follow the pattern: `{Title} {Subject}`

**Key Principles:**
- Identifier represents the **highest level at which scores exist** (typically subject-level)
- **NO vendor name in identifier** (vendor is captured by namespace)
- Use assessment_family for grouping related assessments across subjects
- Include subject when assessments are split by subject
- Use "Composite" for cross-subject assessments

**Examples:**
- ✓ "MAP Growth Reading" (not "NWEA MAP Growth Reading")
- ✓ "STAR-SR" (not "Renaissance STAR-SR")
- ✓ "ACCESS for ELLs Overall" (composite assessment)
- ✓ "ACT Composite" (composite, with subject-specific as objective assessments)

### When to Use Composite Subject

Use "Composite" or "Overall" when:
- Assessment produces a single cross-subject score
- Multiple domain/subject scores roll up to one overall score
- Assessment doesn't split by traditional subjects

**Examples:**
- ACCESS for ELLs: "ACCESS for ELLs Overall" (with language domains as objective assessments)
- ACT: "ACT Composite" (with subjects as objective assessments)
- PSAT/SAT: "PSAT/SAT Composite" (with subjects as objective assessments)

## Namespace Rules

### Use Vendor Domain

Namespaces should use the vendor's actual domain, formatted as a URI:

**Format:** `uri://{vendor-domain}/{assessment-name}/`

**Examples:**
- NWEA MAP: `uri://www.nwea.org/map/`
- Renaissance STAR: `uri://renaissance.com/star/`
- ACT: `uri://act.org/act/`
- ACCESS: `uri://wida.wisc.edu/assessment/access/`
- Dibels: `uri://dibels.uoregon.edu/assessment/dibels/`
- SC READY: `uri://ed.sc.gov/assessment/scready/` (state assessment)

**Important:** Never include vendor name in the assessment identifier itself—the namespace provides the vendor context.

## Assessment Hierarchy Principles

### Capture True Assessment Structure

The hierarchy should reflect how the assessment vendor organizes and reports data:

1. **Top-level Assessment**: Highest level at which scores exist
2. **Objective Assessments**: Subscores, domains, reporting categories, or skill areas
3. **Parent Objective Assessments**: For nested hierarchies (e.g., domain groups containing domains)

### Hierarchy Examples from Existing Bundles

#### NWEA MAP Growth
```
Assessment: "MAP Growth Reading"
├─ ObjectiveAssessment: "Foundational Skills"
├─ ObjectiveAssessment: "Language and Writing"
├─ ObjectiveAssessment: "Literature and Informational Text"
└─ ObjectiveAssessment: "Vocabulary"
```

Split by subject (Reading, Math, Language Usage, Science). Instructional areas are objective assessments.

#### Renaissance STAR
```
Assessment: "STAR-SR"
├─ ObjectiveAssessment: "Comprehension and Analytical Thinking" (parent)
│   ├─ ObjectiveAssessment: "Author's Craft"
│   ├─ ObjectiveAssessment: "Key Ideas and Details"
│   └─ ObjectiveAssessment: "Structural Elements"
└─ ObjectiveAssessment: "Literacy and Decoding" (parent)
    ├─ ObjectiveAssessment: "Decoding"
    └─ ObjectiveAssessment: "Word Knowledge"
```

Split by subject (Reading, Math, Early Literacy). Domain groups with nested skill areas.

#### ACT
```
Assessment: "ACT Composite"
├─ ObjectiveAssessment: "English"
├─ ObjectiveAssessment: "Math"
├─ ObjectiveAssessment: "Reading"
└─ ObjectiveAssessment: "Science"
```

Single composite assessment with subjects as objective assessments.

#### ACCESS for ELLs
```
Assessment: "ACCESS for ELLs Overall"
├─ ObjectiveAssessment: "Listening"
├─ ObjectiveAssessment: "Reading"
├─ ObjectiveAssessment: "Speaking"
└─ ObjectiveAssessment: "Writing"
```

Single overall proficiency with language domains as objective assessments.

#### SC READY
```
Assessment: "SC READY ELA"
├─ ObjectiveAssessment: "Language and Communication"
├─ ObjectiveAssessment: "Reading - Informational"
├─ ObjectiveAssessment: "Reading - Literature"
└─ ObjectiveAssessment: "Research"

Assessment: "SC READY Mathematics"
├─ ObjectiveAssessment: "Data Analysis"
├─ ObjectiveAssessment: "Geometry and Measurement"
├─ ObjectiveAssessment: "Number and Operations"
└─ ObjectiveAssessment: "Algebraic Thinking"
```

Split by subject. Reporting categories as objective assessments.

## Assessment Family

Use `assessmentFamily` to group related assessments across subjects:

**Examples:**
- MAP Growth: Family = "MAP Growth" (groups Reading, Math, Language Usage, Science)
- STAR: Family = "STAR" (groups STAR-SR, STAR-Math, STAR-EL)
- SC READY: Family = "SC READY" (groups ELA, Mathematics, Science, Social Studies)

## studentAssessmentIdentifier

Must be unique within the context of a student + assessment + school year.

**Common patterns:**
- Concatenate multiple columns: `${administration_window}_${test_date}`
- Use vendor-provided unique ID if available
- Ensure uniqueness across test events/administrations

**Important:** Check grain carefully—output must match Ed-Fi StudentAssessment entity grain.

## Governance Review Process

Before implementing a new bundle:

1. **Create governance artifact** using template from Slite
2. **Document hierarchy decisions** with rationale
3. **Submit for committee review** if creating new patterns
4. **Validate against existing bundles** for consistency

### Governance Artifact Template

Available on Slite: "Assessment Bundle Governance Overview"

Includes:
- Assessment identifier structure
- Namespace selection
- Hierarchy diagram
- Descriptor namespace decisions
- Score methodology preservation

## References

- **Slite Documentation:** "Assessment Bundle Governance Overview"
- **Bundle Workflow:** "Writing earthmover bundles" (12-step process)
- **Existing Bundles:** See `assessments/` directory for examples
