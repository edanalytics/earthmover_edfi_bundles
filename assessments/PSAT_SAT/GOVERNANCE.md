# PSAT/SAT Assessment Bundle - Governance Decisions

## Assessment Structure Analysis

### Sample Files Examined
- **PSAT** (N:/sc_2024/.../psat/) - PSAT/NMSQT files - **PSAT 10** (N:/sc_2024/.../psat10/) - PSAT 10 files
- **PSAT 8/9** (N:/sc_2024/.../psat89/) - PSAT 8/9 files- **SAT** (N:/sc_2024/.../sat_enrich/) - SAT files

All files share similar structure with slight variations in score columns (LATEST_PSAT_* vs LATEST_SAT_*).

### Assessment Family
These assessments are part of the **College Board SAT Suite of Assessments**.

**Important: The SAT was redesigned in March 2016, resulting in two different formats in the data:**

**OLD SAT (pre-March 2016):**
- Three sections: Critical Reading, Math, Writing
- Score range: 600-2400 (200-800 per section)
- Data: 2014-2015 files use `LATEST_SAT_CRITICAL_READING`, `LATEST_SAT_MATH`, `LATEST_SAT_WRITING`

**NEW SAT (March 2016+) and PSAT Suite (2015+):**
- Two sections: Evidence-Based Reading and Writing (EBRW), Math
- Score ranges:
  - PSAT 8/9: 240-1440 (120-720 per section)
  - PSAT 10: 320-1520 (160-760 per section)
  - PSAT/NMSQT: 320-1520 (160-760 per section)
  - SAT: 400-1600 (200-800 per section)
- Data: 2016+ files use `LATEST_SAT_EBRW`/`LATEST_PSAT_EBRW`, `LATEST_SAT_MATH_SECTION`/`LATEST_PSAT_MATH_SECTION`

All measure college/career readiness.

## Governance Decisions

### Assessment Identifiers
Following `{Title} {Subject}` pattern with "Composite" for cross-subject assessments:
- **"PSAT 8/9 Composite"** - Grade 8-9 assessment (2015+)
- **"PSAT 10 Composite"** - Grade 10 assessment (2015+)
- **"PSAT/NMSQT Composite"** - Grade 10-11 assessment (2015+, National Merit Scholarship Qualifying Test)
- **"SAT Composite"** - Grade 11-12 assessment (March 2016+ redesigned format)
- **"SAT (Pre-2016) Composite"** - Grade 11-12 assessment (pre-March 2016 format)

**Rationale:** Each is a distinct assessment. Old and new SAT are treated as separate assessments due to fundamentally different structures (3 sections vs 2 sections) and score ranges. "Composite" indicates they measure overall college readiness across multiple content areas.

### Assessment Family
`assessmentFamily: "SAT Suite"`

Groups all four assessments as part of College Board's coordinated assessment system.

### Namespace
`uri://collegeboard.org/sat-suite/`

Uses College Board's domain. The SAT Suite is their branded assessment family.

### Assessment Hierarchy

**NEW SAT/PSAT Suite (2016+ SAT, 2015+ PSAT) - 2-Section Format:**

```
Assessment: "[Test Name] Composite"
├─ ObjectiveAssessment: "Evidence-Based Reading and Writing"
│   ├─ ObjectiveAssessment: "Reading"
│   │   ├─ ObjectiveAssessment: "Command of Evidence"
│   │   └─ ObjectiveAssessment: "Words in Context"
│   └─ ObjectiveAssessment: "Writing and Language"
│       ├─ ObjectiveAssessment: "Expression of Ideas"
│       └─ ObjectiveAssessment: "Standard English Conventions"
├─ ObjectiveAssessment: "Math"
│   ├─ ObjectiveAssessment: "Heart of Algebra"
│   ├─ ObjectiveAssessment: "Problem Solving and Data Analysis"
│   └─ ObjectiveAssessment: "Passport to Advanced Math"
├─ ObjectiveAssessment: "Analysis in History/Social Studies" (Cross-test score)
└─ ObjectiveAssessment: "Analysis in Science" (Cross-test score)
```

**OLD SAT (pre-March 2016) - 3-Section Format:**

```
Assessment: "SAT (Pre-2016) Composite"
├─ ObjectiveAssessment: "Critical Reading" (200-800)
├─ ObjectiveAssessment: "Mathematics" (200-800)
└─ ObjectiveAssessment: "Writing" (200-800)
```

**Hierarchy Notes:**
- New format: Composite → Sections (EBRW, Math) → Tests → Subscores → Cross-test scores
- Old format: Composite → Three independent sections (Critical Reading, Math, Writing)
- Old SAT has simpler structure with no nested subscores in the data files

### Descriptor Namespace Decisions

**Assessment-specific descriptors** (use College Board namespace):
- `assessmentReportingMethodDescriptor`:
  - "Total Score" - Overall composite score
  - "Section Score" - EBRW or Math section score
  - "Test Score" - Reading, Writing & Language, or Math test score
  - "Subscore" - Command of Evidence, Words in Context, etc.
  - "Cross-Test Score" - Analysis in History/Social Studies, Analysis in Science
- `performanceLevelDescriptor`:
  - "Meets Benchmark" - If CCR benchmarks are treated as performance levels
  - Or leave empty if only reporting scores

**Non-assessment-specific descriptors** (use Ed-Fi default namespace `uri://ed-fi.org`):
- `gradeLevelDescriptor`: Eighth grade, Ninth grade, Tenth grade, Eleventh grade, Twelfth grade
- `resultDatatypeTypeDescriptor`: Use `${DESCRIPTOR_NAMESPACE}` parameter (default `uri://ed-fi.org`) for Integer

### Score Preservation
- Preserve original College Board score names exactly:
  - "Total Score" (not "Composite Score")
  - "Evidence-Based Reading and Writing" (full name)
  - "Heart of Algebra" (original subscore name)- NO normalization at integration layer
- College Board uses specific score ranges for each test type - preserve these

### Student Assessment Identifier Pattern
Use: `${test_type}_${test_date}`

Where:
- test_type: "PSAT89" | "PSAT10" | "PSAT" | "SAT"
- test_date: Date of test administration (from LATEST_[PSAT|SAT]_DATE field)

Example: `PSAT_2017-10-11`

Ensures uniqueness per student per test event.

### Test Type Detection Strategy
Auto-detect test type and format from:

1. **Test Type** (PSAT vs SAT):
   - File path contains "psat89", "psat10", "psat", or "sat_enrich"
   - Column name patterns: "LATEST_PSAT_*" vs "LATEST_SAT_*"

2. **SAT Format** (Old 3-section vs New 2-section):
   - **New format (2016+)**: `LATEST_SAT_EBRW` column has values
   - **Old format (pre-2016)**: `LATEST_SAT_CRITICAL_READING` column has values
   - Test date can also help: pre-March 2016 = old format, March 2016+ = new format

3. **PSAT Variant** (8/9 vs 10 vs NMSQT):
   - All use same file structure with "LATEST_PSAT_*" columns
   - Distinguish by file path: "psat89", "psat10", or "psat"

### Grade Level Mapping

**Important**: Students can take any test at any grade level, so grade must be calculated from actual cohort year and test date, not assumed from test type.

**Calculation**:
```
school_year = test_date_year (if Aug-Dec) or test_date_year - 1 (if Jan-Jul)
grade = 12 - (cohort_year - school_year)
```

**Example**:
- Test date: October 2018 → school_year = 2018
- Cohort year: 2019 → grade = 12 - (2019 - 2018) = **11**

**Ed-Fi Mapping**:
- grade 8 → "Eighth grade"
- grade 9 → "Ninth grade"
- grade 10 → "Tenth grade"
- grade 11 → "Eleventh grade"
- grade 12 → "Twelfth grade"

**Note**: Test types indicate intended/designed-for grades, but actual test-takers may be in different grades.

## Implementation Notes

### Null Handling
- Many subscore columns may be empty
- Use build-list-then-loop pattern in templates
- Only include score results that have non-empty values
- At least 1 score result required per StudentAssessment (section scores should always be present)

### File Format Consistency
All four test types use the same basic CSV structure with ~350 columns including:
- Student demographics (NAME_FIRST, NAME_LAST, BIRTH_DATE, etc.)
- Test scores (LATEST_[PSAT|SAT]_* columns)
- Individual question responses (READING_QUES_ANS*, MATH_*_QUES_ANS*, WRITLANG_QUES_ANS*)
- Percentile ranks
- AP course taking patterns
- CCR benchmarks (EBRW_CCR_BENCHMARK, MATH_CCR_BENCHMARK)

### Bundle Strategy
Single bundle with conditional logic to handle all four test types:
- Detect test type from file path or column patterns
- Map to appropriate assessment identifier
- Use same template structure for all (score column names differ slightly)
- Create separate Assessment entities for each test type

## References
- College Board SAT Suite: https://collegereadiness.collegeboard.org/sat-suite-assessments
- Score ranges and content specifications from College Board documentation
- Sample files: N:/south_carolina/sc_2024/assessment_loading/format_conversion/20_final_output/{psat,psat10,psat89,sat_enrich}/
