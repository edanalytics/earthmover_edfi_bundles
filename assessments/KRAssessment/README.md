# Assessment Details

## Assessment Identifier(s)
- KRA (the name of the assessment)

## Assessment Family
- None yet

## Assessment Score Method Descriptors
- uri://ed.sc.gov/assessmentReportingMethodDescriptor#ScaleScore
- uri://ed.sc.gov/assessmentReportingMethodDescriptor#PerformanceLevel

# Hierarchy
![alt text](image.png)

## StudentAssessmentEducationOrganizationAssociation
-SchoolCode is mapped for this entity. 

## Reasoning
The kindergarten readiness assessment is a composite assessment with objectives such as:
- Social Foundation Score
- Language and Literacy Score
- Mathematics Score
- Physical Well-Being and Motor Development Score.

## Summary of Descriptor Fields and Mappings

### assessmentCategoryDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/assessmentCategoryDescriptor#{{assessmentCategoryDescriptor}}`
- **assessments.csv**: kindergarten Readiness

### academicSubjectDescriptor:
- **assessments.jsont**: `uri://ed.sc.gov/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`
- **assessments.csv**: Overall
- Here i am not certain if i should create and academic subject under the assessment namespace or the normal namespace. 
### assessmentReportingMethodDescriptor:
- **assessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#ScaleScore`
- **objectiveAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#ScaleScore`
- **studentAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#ScaleScore`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/AssessmentReportingMethodDescriptor#ScaleScore`
- here the namespace is :  `uri://ed.sc.gov/KRA` 
### resultDatatypeTypeDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`
- **objectiveAssessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`
- **studentAssessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`

### performanceLevelDescriptor:
- **studentAssessments.jsont**: `{{namespace}}/PerformanceLevelDescriptor#{{PerformanceLevelDescriptor}}`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/PerformanceLevelDescriptor#{{PerformanceLevel_SFScore}}, {{PerformanceLevel_LLScore}}, {{PerformanceLevel_MAScore}}, {{PerformanceLevel_PDScore}}`
-Here the performance level descriptors match the top level values :Demonstrating Readiness, Emerging Readiness and Approaching Readiness 
### whenAssessedGradeLevelDescriptor:
- **studentAssessments.jsont**: `{{whenAssessedGradeLevelDescriptor}}`
-Here there is an assumption made the exam is taken by prekindergarten/preschool students : uri://ed-fi.org/GradeLevelDescriptor#Kindergarten
### educationOrganizationAssociationTypeDescriptor:
- **educationOrganizationAssociationTypeDescriptor**: `uri://ed-fi.org/EducationOrganizationAssociationTypeDescriptor#Administration`

### Other mapping decisions  
- using *PS_StudentID vs *StudentSUNS for the StudentId mapping 
- using *DistrictCode vs SchoolCode for the studentAssessmentEducationOrganizationAssociation entity.

