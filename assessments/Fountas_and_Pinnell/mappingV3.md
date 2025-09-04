# Fountas & Pinnell Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - Fountas_and_Pinnell

## Assessment Family
Fountas and Pinnell

## Namespace
Namespace: uri://fountasandpinnell.com/bas

# Objectives
## Objectives Identifiers
 - F&P_Text_Reading
 - F&P_Comprehension



# Performance levels
For F&P_Text_Reading objective: Lexile Level
 - BR-25
 - 26-199
 - 200-299
 - 300-499
 - 500-699
 - 700-749
 - 750-949
 - 950-Up

For F&P_Comprehension objective: Comprehension Level
 - Approaching Proficiency
 - Limited Proficiency
 - Proficient
 - Satisfactory
 - Excellent
 - Limited
 - Unsatisfactory
 

## Assessments Score Method Descriptors
For F&P_Text_Reading objective:
 - Fluency Level
 - Self Correction Rate
 - Words Per Minute
 - Text Reading Accuracy
 - Text Reading Level
 - Early Literacy Behaviors
 - Letter Recognition
 - Initial Sounds
 - High Frequency Words
 - Rhyming Assessment
 - Word Writing
 - Lexile Level
 
  
For F&P_Comprehension objective:
 - Comprehension
 - Comprehension2
 - Meaning
 - Visual
 - ComprehensionLevel
  
## Genre  how to map?  SerialNumber of eventDescription?
- Fiction
- Nonfiction

## TextReading column ????? As score for F&P_Text_Reading objective
From Pre-A, A, B .... Z
It seems to be difficulty ranges.  Should I map?



## Reasoning
The Fountas & Pinnell Benchmark Assessment System (BAS) is designed to provide educators with a comprehensive and systematic approach to assess a student's reading proficiency. Rooted in the belief that effective literacy instruction begins with deep insight into each student's reading behaviors and comprehension strategies, the assessment emphasizes individualized evaluation through authentic reading tasks.

# Data Sources

## Input Requirements

## Bundle Seeds
  - objectiveAssessments.csv
  - assessmentReportingMethodDescriptors.csv
  - assessments.csv
  - gradeMappings.csv
  - performanceLevelDescriptors.csv

## Template Files
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
- uri://fountasandpinnell.com/bas/AssessmentCategoryDescriptor#Performance assessment
  
### assessmentReportingMethodDescriptor:
- Namespace: uri://fountasandpinnell.com/bas/AssessmentReportingMethodDescriptor



# Output Files
- assessmentCategoryMethodDescriptors.jsonl
- assessmentReportingMethodDescriptors.jsonl
- assessments.jsonl
- objectiveAssessments.jsonl
- performanceLevelDescriptors.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl


# Dependencies
- Requires Earthmover version 0.3.8 or higher