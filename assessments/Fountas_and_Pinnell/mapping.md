# Fountas & Pinnell Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - Fountas_and_Pinnell

## Assessment Family
Fountas and Pinnell

## Namespace
Namespace: uri://fountasandpinnell.com/bas

# Overall scores
## Assessment Score Method Descriptors
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
 - Comprehension
 - Comprehension2
 - Meaning
 - Visual
 - Comprehension Level
 - Genre


# Overall Performance levels
For Lexile Level reporting method
 - BR-25
 - 26-199
 - 200-299
 - 300-499
 - 500-699
 - 700-749
 - 750-949
 - 950-Up

For Comprehension Level reporting method
 - Approaching Proficiency
 - Limited Proficiency
 - Proficient
 - Satisfactory
 - Excellent
 - Limited
 - Unsatisfactory
 
## Reasoning
The Fountas & Pinnell Benchmark Assessment System (BAS) is designed to provide educators with a comprehensive and systematic approach to assess a student's reading proficiency. Rooted in the belief that effective literacy instruction begins with deep insight into each student's reading behaviors and comprehension strategies, the assessment emphasizes individualized evaluation through authentic reading tasks.

# Data Sources

## Input Requirements

## Bundle Seeds
  - assessmentReportingMethodDescriptors.csv
  - assessments.csv
  - mapping_grade.csv
  - performanceLevelDescriptors.csv
  - assessmentCategoryDescriptors.csv

## Template Files
  - assessmentReportingMethodDescriptors
  - assessments.jsont
  - descriptors.jsont
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
- uri://fountasandpinnell.com/bas/AssessmentCategoryDescriptor#Early Learning - Language and literacy development
  
### assessmentReportingMethodDescriptor:
- Namespace: uri://fountasandpinnell.com/bas/AssessmentReportingMethodDescriptor

# Output Files
- assessmentCategoryMethodDescriptors.jsonl
- assessmentReportingMethodDescriptors.jsonl
- assessments.jsonl
- performanceLevelDescriptors.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl


# Dependencies
- Requires Earthmover version 0.3.8 or higher
