# ACTWorkKeys Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
- Each ACTWorkKeys assessment component is mapped to a unique Assessment file.
- Assessment Identifier:
  - ACTWorkKeysPre2022
  - ACTWorkKeys2022

## Assessment Family
ACTWorkKeys

## Assessments Score Method Descriptors
For each assessment there will be two score method descriptors:
 - Level Score (string)
 - Scale Score (integer)

## Composite Score
- Overall score is reported as the NCRC credential, mapped from Certificate Level.
- Reported under `scoreResults` in the `studentAssessment` record. 
  
# Hierarchy
![alt text](hierarchy.png)

## Reasoning
The ACT WorkKeys Assessment is administered to measure foundational career readiness skills that are essential across a wide range of occupations. The purpose of this assessment is to evaluate students' applied knowledge in real-world scenarios.

This assessment supports instructional and accountability goals by providing reliable, standardized data that informs educational planning, workforce alignment, and credentialing decisions. The results can be used to help students identify career pathways, assist educators in tailoring instruction, and help employers evaluate workforce preparedness.

This bundle processes ACT WorkKeys assessment data, transforming it into Ed-Fi compatible assessment and student assessment records. The bundle handles multiple ACTWorkKeys objective domains including Applied Math, Workplace Documents and Graphic Literacy (2022) or Applied Math, Locating Information, and Reading for Information (pre2022).

Each objective assessment is scored with both a Level Score (which may contain non-numeric values like `< 3`) and a Scale Score. These feed into the overall credential score (ACCTWK_NCRC Credential).

**Note:** The ACT WorkKeys file structure differs between assessment years. For example, the **2022** file format groups scores by objective per row, while **pre-2022** files provide scores in a single row with multiple columns. This bundle dynamically supports both formats, adjusting processing logic based on the year of the assessment.

# Data Sources

## Input Requirements
- Primary source file containing student ACTWorkKeys assessment data with the following required columns:
  - Student unique identifier.
  - Assessment administration date
  - Objective assessment identifier
  - Level Score and Scale Score, one pair per objective.
  - Certificate Level, used for the composite score.

## Bundle Seeds
- `assessments.csv`: Contains assessment metadata
- `assessmentReportingMethodDescriptors.csv`: Contains assessment reporting methods
- `assessmentCategoryDescriptors.csv`: Contains category descriptors
- `assessmentPlatformTypeDescriptors.csv`: Platform descriptors (WKPP/WKIV)
- `gradeLevelMapping.csv`: Grade level values by testing type
- `certificateLevelMapping.csv`: Maps NCRC levels (Bronze, Silver, etc.)
- `accommodationDescriptors.csv`: Identifies accommodations like Text-to-Speech
- `objectiveAssessments.csv`: Defines assessment objectives


# Ed-Fi Mapping
This bundle produces the following Ed-Fi resources:


## StudentAssessments
- studentAssessmentIdentifier: Generated using MD5 hash of assessmentIdentifier, studentUniqueId, and assessment date
- administrationDate: Mapped from testdate ? Test Date
- schoolYear: Mapped from testdate
- studentReference: Mapped from stateid / Examinee ID
- scoreResults:
  - assessmentReportingMethodDescriptor: Mapped from descriptor source
  - resultDatatypeTypeDescriptor: Set to "Integer" for scale scores, and "String" for level score
  - result: Mapped from corresponding assessment score column

## Summary of Descriptor Fields and Mappings


### gradeLevelDescriptor:
- Namespace: `uri://ed-fi.org/GradeLevelDescriptor`
- If "WorkKeys Source" = WKPP:
  - 1 = 7th Grade → Seventh Grade
  - 2 = 8th Grade → Eighth Grade
  - 3 = 9th Grade → Ninth Grade
  - 4 = 10th Grade → Tenth Grade
  - 5 = 11th Grade → Eleventh Grade
  - 6 = 12th Grade → Twelfth Grade
  - 7 = H.S. Grad. → Postsecondary
  - 8 = GED → Postsecondary
  - 9 = Other Secondary → Postsecondary
  - 10 = 1st Year Postsecondary → Postsecondary
  - 11 = 2nd Year Postsecondary → Postsecondary
  - 12 = 3rd Year Postsecondary → Postsecondary
  - 13 = 4th Year Postsecondary → Postsecondary
  - 14 = 5th Year or Higher Post. → Postsecondary
  - 15 = Other Postsecondary → Postsecondary

- If "WorkKeys Source" = WKIV:
  - 8th Grade or below → Eighth Grade
  - 9th Grade → Ninth Grade
  - 10th Grade → Tenth Grade
  - 11th Grade → Eleventh Grade
  - 12th Grade → Twelfth Grade
  - Dual enrollment-11th grade & college → Eleventh Grade
  - Dual enrollment-12th grade & college → Twelfth Grade
  - Trade/Proprietary school → Postsecondary
  - Community College → Postsecondary
  - Postsecondary-4-Year Institutions: Freshman → Postsecondary
  - Postsecondary -4-Year Institutions: Sophomore → Postsecondary
  - Postsecondary-4-Year Institutions: Junior → Postsecondary
  - Postsecondary-4-Year Institutions: Senior → Postsecondary
  - Postsecondary-4-Year Institutions: Postgraduate → Postsecondary


### assessmentCategoryDescriptor:
- `uri://act.org/AssessmentCategoryDescriptor#HS_CAREER_COLLEGE`

### assessmentReportingMethodDescriptor:
- Level Score: `uri://act.org/AssessmentReportingMethodDescriptor#Level Score`
- Scale Score: `uri://act.org/AssessmentReportingMethodDescriptor#Scale Score`
- NCRC Credential: `uri://act.org/AssessmentReportingMethodDescriptor#ACCTWK_NCRC Credential`

### resultDatatypeTypeDescriptor:
- Scale Score: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`
- Level Score: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#String`

### assessmentPlatformTypeDescriptors:
- WKPP: `uri://act.org/PlatformTypeDescriptor#WKPP`
- WKIV: `uri://act.org/PlatformTypeDescriptor#WKIV`

### accommodationDescriptors:
- If `Manifest Name` contains " - Text To Speech":
  - `uri://act.org/accommodationDescriptors#Test administration accommodation`

# Output Files

- accommodationDescriptors.jsonl
- assessmentReportingMethodDescriptors.jsonl
- assessmentCategoryMethodDescriptors.jsonl
- assessments.jsonl
- objectiveAssessments.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl
- assessmentPlatformTypeDescriptors.jsonl
- assessmentGradelevelDescriptors.jsonl

# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:
  - ./templates/assessments.jsont
  - ./templates/objectiveAssessments.jsont
  - ./templates/descriptors.jsont
  - ./templates/studentAssessments.jsont
  - ./templates/studentAssessmentEducationOrganizationAssociations.jsont

