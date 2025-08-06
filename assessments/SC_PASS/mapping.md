# SCPASS Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - SC_PASS_Science_{year}
  - SC_PASS_Social_Studies_{year} (Not administered in 2020-2021 and 2021-2022)

Since this is a state summative, they need to include the year.


## Assessment Family
SCPASS

## Namespace
Namespace: uri://datarecognitioncorp.com/Assessments/SCPASS

# Objectives
## Objectives Identifiers
  - Science Standard 1
  - Science Standard 2
  - Science Standard 3
  - Science Standard 4
  - Science Standard 5
  - Science Standard 6
  - Social Studies Standard 1
  - Social Studies Standard 2
  - Social Studies Standard 3
  - Social Studies Standard 4
  - Social Studies Standard 5
  - Social Studies Standard 6
  - Social Studies Standard 7
 

# Performance levels
## Overall
Science performance levels
 - 1 = does not meet expectations 
 - 2 = approaches expectations
 - 3 = meets expectations
 - 4 = exceeds expectations

Social studies performance levels
 - 1 = not met 
 - 2 = met
 - 3 = exemplary 

## Objectives performance level
 - 1= shows weaknesses and a need for further instruction
 - 2= may benefit from additional activities
 - 3= shows strengths


## Assessments Score Method Descriptors
- For scores:
 - SocSS: 	Scale Score
 - SocRCWAbs: Report Card Weight—Absolute
 - SocAg: Aggregated Student
 - SciSS: 	Scale Score
 - SciRCWAbs: Report Card Weight—Absolute
 - SciAg: Aggregated Student
- For performance levels:
 - SocLev1
 - SocLev2
 - SocLev3
 - SocLev4
 - SocLev5
 - SocLev6
 - SocLev7
 - SocLev
 - SciLev1
 - SciLev2
 - SciLev3
 - SciLev4
 - SciLev5
 - SciLev6
 - SciLev7
 - SciLev

## Reasoning
SCPASS is designed to measure student performance against the South Carolina Academic Standards and indicators — in other words, what the state expects students to learn and demonstrate in science and social studies classes.

# Data Sources

## Input Requirements

## Bundle Seeds
  - accommodationDescriptors.csv
  - assessmentPeriodDescriptors.csv
  - objectiveAssessments.csv
  - assessmentReportingMethodDescriptors.csv
  - assessments.csv
  - gradeMappings.csv
  - performanceLevelDescriptors.csv

## Template Files
  - accommodationDescriptors.jsont
  - assessmentCategoryDescriptors
  - assessmentReportingMethodDescriptors
  - assessments.jsont
  - descriptors.jsont
  - objectivesAssessments.jsont
  - studentAssessmentEducationOrganizationAssociations.jsont
  - studentAssessments.jsont


## Summary of Descriptor Fields and Mappings

### gradeLevelDescriptor:
 - uri://ed-fi.org/GradeLevelDescriptor#UnGraded
 - uri://ed-fi.org/GradeLevelDescriptor#Third grade
 - uri://ed-fi.org/GradeLevelDescriptor#Fourth grade
 - uri://ed-fi.org/GradeLevelDescriptor#Fifth grade
 - uri://ed-fi.org/GradeLevelDescriptor#Sixth grade
 - uri://ed-fi.org/GradeLevelDescriptor#Seventh grade
 - uri://ed-fi.org/GradeLevelDescriptor#Eighth grade


### assessmentCategoryDescriptor:
- uri://datarecognitioncorp.com/Assessments/SCPASS/AssessmentCategoryDescriptor#Science
- uri://datarecognitioncorp.com/Assessments/SCPASS/AssessmentCategoryDescriptor#Social Studies
  
### assessmentReportingMethodDescriptor:
- Namespace: uri://datarecognitioncorp.com/Assessments/SCPASS/AssessmentReportingMethodDescriptor

### accommodationDescriptors:
Namespace: uri://datarecognitioncorp.com/Assessments/SCPASS/AccommodationDescriptor
  - SciAcc1	Science Setting
  - SciAcc2	Science Timing
  - SciAcc3	Science Scheduling
  - SciAcc4	Science Presentation – Oral/Signed Administration Script
  - SciAcc5	Science Presentation – Oral Administration TTS
  - SciAcc6	Science Presentation – Signed Administration VSL
  - SciAcc7	Science Presentation – Other
  - SciAcc8	Science Response Options
  - SciAcc9	Science – Supplemental Materials or Devices
  - SciAcc10	
  - SciAcc11	
  - SciESLAcc1	Science ESL Bilingual Dictionary
  - SciESLAcc2	Science ESL Directions Translated
  - SciESLAcc3	Science ESL Individual and Small Group Administration
  - SciESLAcc4	Science ESL Oral Administration
  - SciESLAcc5	Science ESL Scheduling
  - SciESLAcc6	Science ESL Timing


  - SocAcc1	Social Studies Setting
  - SocAcc2	Social Studies Timing
  - SocAcc3	Social Studies Scheduling
  - SocAcc4	Social Studies Presentation – Oral/Signed Administration Script
  - SocAcc5	Social Studies Presentation – Oral Administration TTS
  - SocAcc6	Social Studies Presentation – Signed Administration VSL
  - SocAcc7	Social Studies Presentation – Other
  - SocAcc8	Social Studies Response Options
  - SocAcc9	Social Studies Supplemental Materials or Devices
  - SocAcc10	
  - SocAcc11	
  - SocESLAcc1	Social Studies ESL Bilingual Dictionary
  - SocESLAcc2	Social Studies ESL Directions Translated
  - SocESLAcc3	Social Studies ESL Individual and Small Group Administration
  - SocESLAcc4	Social Studies ESL Oral Administration
  - SocESLAcc5	Social Studies ESL Scheduling
  - SocESLAcc6	Social Studies ESL Timing


# Output Files
- accommodationDescriptors.jsonl
- assessmentCategoryMethodDescriptors.jsonl
- assessmentPeriodDescriptors.jsonl
- assessmentReportingMethodDescriptors.jsonl
- assessments.jsonl
- objectiveAssessments.jsonl
- performanceLevelDescriptors.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl


# Dependencies
- Requires Earthmover version 0.3.8 or higher
