# Assessment Details
- The Advanced Placement (AP) exam is offered by College Board. AP gives students the chance to tackle college-level work while they are still in high school and earn college credit and placement. 

## Assessment Family
- Advance Placement

## Assessment Identifier(s)
- Assessment identifier concatenates AP with the Exam Code field, i.e. AP - 7.

## Assessment Score
- Student receives an exam score for each AP exam. The minimum Score is 1 and maximum score is 5. These are mapped with the AssessmentReportingMethodDescriptor of AP Score and ResultDatatypeTypeDesciptor of Integer.

## Assessment Reporting Method Descriptors
- uri://collegeboard.org/AssessmentReportingMethodDescriptor#AP Score
- uri://collegeboard.org/AssessmentReportingMethodDescriptor#AP Award
- uri://collegeboard.org/AssessmentReportingMethodDescriptor#AP Irregularity Code

## Assessment Performance Levels
Student may or may not receive an AP award based on their performance on multiple exams. AP Awards are mapped as performance Levels. below are the AP Award types that have been mapped.
- 01 AP Scholar 
- 02 AP Scholar with Honor
- 03 AP Scholar with Distinction
- 07 AP International Diploma
- 13 AP Capstone Diploma
- 14 AP Seminar and Research Certificate

# Hierarchy
The grain of the assessment is at the exam code (subject) level. There is only one score available for each exam and there are no objective assessments.

## Assessment Academic Subject Descriptor
- There are several academic subjects associated with the AP exams, the mappings for which are provided. 
- Note: These will need to be verified and correct values added for your implementation if you choose to use the EdFi descriptor values.
    - Computer Science AB mapped to Science
    - Microeconomics mapped to Other
    - Macroeconomics mapped to Other
    - English Language and Composition mapped to English
    - English Literature and Composition mapped to English
    - Environmental Science mapped to Life and Physical Sciences
    - European History mapped to Social Sciences and History
    - French Language and Culture mapped to Foreign Language and Literature
    - French Literature mapped to Foreign Language and Literature
    - United States Government and Politics mapped to Social Sciences and History
    - Comparative Government and Politics mapped to Social Sciences and History
    - Latin mapped to Foreign Language and Literature
    - Latin Literature mapped to Foreign Language and Literature
    - Italian Language and Culture mapped to Foreign Language and Literature
    - Japanese Language and Culture mapped to Foreign Language and Literature
    - Precalculus mapped to Mathematics
    - Calculus AB mapped to Mathematics
    - Calculus BC mapped to Mathematics
    - Calculus BC: AB Subscore mapped to Mathematics
    - Music Theory mapped to Fine and Performing Arts
    - Music Aural Subscore mapped to Fine and Performing Arts
    - Music Non-Aural Subscore mapped to Fine and Performing Arts
    - Physics B mapped to Science
    - Physics C: Mechanics mapped to Science
    - Physics C: Electricity and Magnetism mapped to Science
    - Physics 1 mapped to Science
    - Physics 2 mapped to Science
    - Psychology mapped to Social Sciences and History
    - Spanish Language and Culture mapped to Foreign Language and Literature
    - Spanish Literature and Culture mapped to Foreign Language and Literature
    - Statistics mapped to Mathematics
    - World History: Modern mapped to Social Sciences and History

## StudentAssessmentIdentifier
- This is derived by concatenating the assessmentIdentifier, Student Identifier and Admin Year then hashing the value with md5. "assessmentIdentifier ~ '-' ~ studentUniqueId ~ '-' ~  SchoolYear"
- For example for AP - 7 taken by student identifier 9999 Admin Year 24, the StudentAssessmentIdentifier is the md5 hash of "AP - 7-9999-24".

## StudentAssessmentEducationOrganizationAssociation
- Populate school associations using the AI code field via the StudentAssessmentEducationOrganizationAssociation entity.
- EducationOrganizationAssociation type of Enrollment.

## Reasoning
- The AdministrationDate in the StudentAssessment resource is derived by concatenating May 01, to the Admin Year fields, i.e ‘05-01-’~Admin Year.
- The fields Irregularity Code #1  and Irregularity Code #2 are mapped to the ScoreResult in the StudentAssessment resource. Using the AssessmentReportingMethod; AP Irregularity Code and ResultDataType of Level.
- The Fields Award Type 1/Award Type 2/Award Type 3/Award Type 4/Award Type 5/Award Type 6 are mapped to the PerformanceLevel in the StudentAssessment resource. This will allow the multiple AwardTypes to be loaded for each exam per administration when provided. Using the AssessmentReportingMethod; AP Award.
- There are records in the vendor file where the Student Identifier field is empty, these records will be excluded in the Bundle because StudentUniqueId is a required field.
- There are records in the vendor file where the value provided for the Student Identifier is a string like the student name. These records will NOT be excluded from the bundle, however they probably will not be loaded since the values provided will not match the StudentUniqueId from the API/ODS.

## Summary of Descriptor Fields and Mappings

### assessmentCategoryDescriptor:
- **assessments.jsont**: `uri://collegeboard.org/AssessmentCategoryDescriptor#{{assessmentCategoryDescriptor}}`
- **assessments.csv**: Advanced Placement

### assessmentPeriodDescriptor:
- **assessments.jsont**: `uri://collegeboard.org/AssessmentPeriodDescriptor#{{assessmentPeriodDescriptor}}`
- **assessments.csv**: Spring

### assessmentReportingMethodDescriptor:
- Here the namespace is :  `uri://collegeboard.org`
- **assessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#AP Award`
- **assessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#AP Score`
- **studentAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#AP Award`
- **studentAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#AP Score`
- **studentAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#AP Irregularity Code`
 
### resultDatatypeTypeDescriptor:
- **studentAssessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Level`
- **studentAssessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`

### performanceLevelDescriptor:
- **Assessments.jsont**: `uri://collegeboard.org/PerformanceLevelDescriptor#{{AwardType}}`
- **studentAssessments.jsont**: `uri://collegeboard.org/PerformanceLevelDescriptor#{{AwardType}}`

### academicSubjectDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`

### GradeLevelDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/GradeLevelDescriptor#{{grade_json}}`
- **studentAssessments.jsont**: `uri://ed-fi.org/GradeLevelDescriptor#{{whenAssessedGradeLevelDescriptor}}`

### educationOrganizationAssociationTypeDescriptor:
- **educationOrganizationAssociationTypeDescriptor**: `uri://ed-fi.org/EducationOrganizationAssociationTypeDescriptor#Enrollment`
