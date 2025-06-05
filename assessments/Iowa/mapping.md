# IOWA Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - IOWA-Survey
  - IOWA-Complete

## Assessment Family
IOWA

## Namespace
DLP uses DESCRIPTOR_NAMESPACE_OVERRIDE=uri://ed-fi.org/ as default for all the elements and sends as parameter any descriptor to replace with. 
So, I think we can fix it by replacing the namespace for assessment, objectiveAssessment, performanceLevelDescriptors, assessmentCategoryDescriptor, assessmentReportingMethodDescriptor, assessmentPeriodDescriptor, accommodationDescriptors.

Possible namespace: uri://www.riversideinsights.com/Iowa

# Objectives
## Objectives Identifiers
For each assessment there are these objectives identifiers:
 - R: Reading
 - V: Vocabulary
 - SP: Spelling
 - CP: Capitalization
 - PC: Punctuation
 - L: Language (levels 05-08)
 - WE: Written Expression (levels 09-17)
 - CW: Conventions of Writing
 - ET: ELA Total
 - WA: Word Analysis
 - Li: Listening
 - XET: Extended ELA Total
 - M: Mathematics (or MT without Comp)
 - MC: Computation
 - MT: Math Total (with Comp)
 - CT: Core Composite (with ELA | with Comp)
 - XCT: Core Composite (with Extended ELA | with Comp)
 - CT-: Core Composite (with ELA without Comp)
 - XCT-: Core Composite (with Extended ELA without Comp)
 - SS: Social Studies
 - SC: Science
 - CC: Complete Composite (with ELA | with Comp)
 - XCC: Complete Composite (with Extended ELA | with Comp)
 - CC-: Complete Composite (with ELA without Comp)
 - XCC-: Complete Composite (with Extended ELA without Comp)
 - RW: Reading Words for Level 06 only (this is Reading Part 1 reported in Slot 1)
 - RC: Reading Comprehension for Level 06 only (this is Reading Part 2 reported in Slot 1)
 - RT: Reading Total
 - LT: Language Total
 - N/A: Not used
 - N/A-2: Not used

## Performance levels
 - 1 = Completion Criteria met 
 - 0 = Completion Criteria not met
 - -1 = Test not included in the Battery

## Assessments Score Method Descriptors
There are these score method descriptors:

The following scores are not tied to an objective, so I can assume that they are overall scores
 - Predicted SAT Critical Reading High (overall)
 - Predicted SAT Critical Reading Low (overall)
 - Predicted SAT Math High (overall)
 - Predicted SAT Math Low (overall)
 - Predicted ACT Composite High (overall)
 - Predicted ACT Composite Low (overall)

The following scores are tied to an objective, so they are objectives scores
 - Number Attempted
 - Completion Criteria, also modeled as Performance Level
 - Raw Score
 - Standard Score
 - Grade Equivalent
 - National Percentile Rank
 - National Curve Equivalent
 - National Stanine
 - Predicted Standard Score
 - Predicted Grade Equivalent
 - Predicted National Percentile Rank
 - Predicted Standard Score Diffs
 - Predicted Grade Equivalent Diffs
 - Local Percentile Rank
 - Local Stanine
 - SDCD Levels Percent Correct
 - CSS Domain Percent Correct
 - College Readiness
 - Standard Score based on 2005 norms
 - Standard Score based on 2011 norms
 - Grade Equivalent based on 2005 norms
 - Grade Equivalent based on 2011 norms
 - National Percentile Rank based on 2005 norms
 - National Percentile Rank based on 2011 norms
 - National Stanine based on 2005 norms
 - National Stanine based on 2011 norms
 - CSS without Computation Domain Percent Correct
 - State Predicted Scale Score: Low Score of Range
 - State Predicted Scale Score: High Score of Range
 - State Predicted Scale Score
 

 
# Hierarchy
![alt text](hierarchy.png)

## Reasoning




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
  - Online desktop or laptop
  - Online tablet
  - Large Print
  - Proctor led
  - Self-paced
  - Audio Type
  - English Language Administration
  - Spanish Language Administration
  - Extended Time

# Output Files

- assessmentReportingMethodDescriptors.jsonl
- assessmentCategoryMethodDescriptors.jsonl
- assessments.jsonl
- objectiveAssessments.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl
- assessmentPlatformTypeDescriptors.jsonl

# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:
  - ./templates/assessments.jsont
  - ./templates/objectiveAssessments.jsont
  - ./templates/descriptors.jsont
  - ./templates/studentAssessments.jsont
  - ./templates/studentAssessmentEducationOrganizationAssociations.jsont

