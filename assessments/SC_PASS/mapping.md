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
 - SS: 	Scale Score
 - RCWAbs: Report Card Weight—Absolute
 - Ag: Aggregated Student
 - 
- For performance levels:
 - Lev1
 - Lev2
 - Lev3
 - Lev4
 - Lev5
 - Lev6
 - Lev7
 - Lev (overall)


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
  - Acc1	Science Setting
  - Acc2	Science Timing
  - Acc3	Science Scheduling
  - Acc4	Science Presentation – Oral/Signed Administration Script
  - Acc5	Science Presentation – Oral Administration TTS
  - Acc6	Science Presentation – Signed Administration VSL
  - Acc7	Science Presentation – Other
  - Acc8	Science Response Options
  - Acc9	Science – Supplemental Materials or Devices
  - Acc10	
  - Acc11	
  - ESLAcc1	Science ESL Bilingual Dictionary
  - ESLAcc2	Science ESL Directions Translated
  - ESLAcc3	Science ESL Individual and Small Group Administration
  - ESLAcc4	Science ESL Oral Administration
  - ESLAcc5	Science ESL Scheduling
  - ESLAcc6	Science ESL Timing


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
