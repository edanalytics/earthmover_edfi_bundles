# Assessment Details

## Assessment
This bundle was designed for 2 types of STAMP test; STAMP 4S and STAMP WS.

## Assessment Family
- STAMP

## Assessment Identifier(s)
- There are two Assessmentidentifier derived based on the two test STAMP 4S and STAMP WS.
    - STAMP 4S
    - STAMP WS

## Assessment Language(s)
- There are several languages associated with the two test STAMP 4S and STAMP WS, the mappings for which are provided.
- Note: Highlighted languages do not have a one to one mapping with the SC Ed language descriptor values. These will need to be verified and correct values added for your implementation if you are using the SC Ed language descriptor values.
- STAMP 4S languages:
    - **American Sign Language mapped to ASL code value for Language Descriptor.**
    - Arabic mapped to ARB code value for Language Descriptor.
    - **Chinese Simplified mapped to CHN SIM code value for Language Descriptor.**
    - Chinese Traditional mapped to CHN code value for Language Descriptor.
    - French mapped to FRN code value for Language Descriptor.
    - German mapped to GRM code value for Language Descriptor.
    - Hebrew mapped to HEB code value for Language Descriptor.
    - Hindi mapped to HND code value for Language Descriptor.
    - Italian mapped to ITA code value for Language Descriptor.
    - Japanese mapped to JPN code value for Language Descriptor.
    - Korean mapped to KRN code value for Language Descriptor.
    - **Latin mapped to LAT code value for Language Descriptor.**
    - **Mandarin Simplified mapped to MND SIM code value for Language Descriptor.**
    - Mandarin Traditional mapped to MND code value for Language Descriptor.
    - Polish mapped to POL code value for Language Descriptor.
    - Portuguese mapped to PRT code value for Language Descriptor.
    - Russian mapped to RSN code value for Language Descriptor.
    - Spanish mapped to SPN code value for Language Descriptor.
    - **Spanish Monolingual mapped to SPN MONO code value for Language Descriptor.**
    - Swahili (3 skill) mapped to SWA code value for Language Descriptor.
    - Yoruba (3 skill) mapped to YOR code value for Language Descriptor.
- STAMP WS languages:
    - Amharic mapped to AMH code value for Language Descriptor.
    - Armenian mapped to ARM code value for Language Descriptor.
    - Chin (Hakha) mapped to HKC code value for Language Descriptor.
    - **Chuukese mapped to CHK code value for Language Descriptor.**
    - Czech mapped to CZE code value for Language Descriptor.
    - Filipino(Tagalog) mapped to TGL code value for Language Descriptor.
    - **Haitian-Creole mapped to HAT code value for Language Descriptor.**
    - **Hawaiian mapped to HAW code value for Language Descriptor.**
    - Hmong mapped to HMN code value for Language Descriptor.
    - **Ilocano mapped to ILO code value for Language Descriptor.**
    - Kannada mapped to KAN code value for Language Descriptor.
    - **Marshallese mapped to MAH code value for Language Descriptor.**
    - Marathi mapped to MAR code value for Language Descriptor.
    - Samoan mapped to SMO code value for Language Descriptor.
    - **Somali Maay Maay mapped to SOM MAY code value for Language Descriptor.**
    - **Somali Maxaa mapped to SOM MAX code value for Language Descriptor.**
    - Tamil mapped to TAM code value for Language Descriptor.
    - Telugu mapped to TEL code value for Language Descriptor.
    - Turkish mapped to TRK code value for Language Descriptor.
    - Urdu mapped to URD code value for Language Descriptor.
    - Vietnamese mapped to VTN code value for Language Descriptor.
    - **Yup'ik mapped to YPK code value for Language Descriptor.**
    - **Zomi mapped to ZOM code value for Language Descriptor.**

## Assessment Assessment Reporting Method Descriptors
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Composite Score

## ObjectiveAssessment Assessment Reporting Method Descriptors
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Scale Score
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Performance Level

## Assessment Academic Subject Descriptor
- uri://ed.sc.gov/AcademicSubjectDescriptor#Language Proficiency

## ObjectiveAssessment Academic Subject Descriptor
- uri://ed.sc.gov/AcademicSubjectDescriptor#Reading
- uri://ed.sc.gov/AcademicSubjectDescriptor#Writing
- uri://ed.sc.gov/AcademicSubjectDescriptor#Listening
- uri://ed.sc.gov/AcademicSubjectDescriptor#Speaking
- The mapping for the Objectives to academic subject descriptor are identified below. 
    - objective Reading mapped to academic subject descriptor Reading.
    - objective Writing mapped to academic subject descriptor Writing.
    - objective Listening mapped to academic subject descriptor Listening.
    - objective Speaking mapped to academic subject descriptor Speaking.

# Hierarchy
![alt text](image.png)

## StudentAssessmentIdentifier
- This is derived by concatenating the assessmentIdentifier, test taker id and start date then hashing the value with md5. "assessmentIdentifier ~ '-' ~ studentUniqueId ~ '-' ~  StartDate"
- For example for Stamp 4S in the language Spanish taken by student with test taker id 9999 on date 12/1/2024, the StudentAssessmentIdentifier is the md5 hash of "STAMP 4S-Spanish-9999-12/1/2024".

## StudentAssessmentEducationOrganizationAssociation
- District is mapped for this entity with EducationOrganizationAssociation type of Attribution.

## SchoolYear
- The School Year is derived by taking the year portion of the Start Date. 
- If the month of the Start Date is >=8 then SchoolYear is the Year from the Start Date + 1 else SchoolYear is Year from the Start Date.
- For example, the start date of 12/1/2024 would produce the School Year 2025 (2024 + 1).

## Reasoning
- The STAndards-based Measurement of Proficiency (STAMP) is an adaptive composite assessment with objectives:
    - Reading mapped to Reading academic subject in the South Carolina Academic subject namespace.
    - Writing mapped to Writing academic subject in the South Carolina Academic subject namespace.
    - Listening mapped to Listening academic subject in the South Carolina Academic subject namespace.
    - Speaking mapped to Speaking academic subject in the South Carolina Academic subject namespace.
- The field 'Test Code' found in the Sample STAMP 4S file was mapped to the IdentificationCodes in the Assessment resource.
- The field 'Testing Group' found in the Sample STAMP 4S file was mapped to SerialNumber in the StudentAssessment resource.
- The field 'Test Length' found in the Sample STAMP 4S file was mapped to AssessedMinutes in the StudentAssessment resource.
- The fields indicating 'Length of Time' found in the Sample STAMP 4S file were mapped to AssessedMinutes in the StudentObjectiveAssessment collection.
- The field 'Status' found in the Sample STAMP 4S file was mapped to EventDescription in the StudentAssessment resource.

## Summary of Descriptor Fields and Mappings

### assessmentCategoryDescriptor:
- **assessments.jsont**: `uri://avantassessment.com/AssessmentCategoryDescriptor#{{assessmentCategoryDescriptor}}`
- **assessments.csv**:Language proficiency test

### assessmentPeriodDescriptor:
- **assessments.jsont**: `uri://avantassessment.com/AssessmentPeriodDescriptor#{{assessmentPeriodDescriptor}}`
- **assessments.csv**:Fall, Spring

### assessmentReportingMethodDescriptor:
- Here the namespace is :  `uri://avantassessment.com`
- **assessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#Performance Level`
- **objectiveAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#Performance Level`
- **studentAssessments.jsont**: `{{namespace}}/AssessmentReportingMethodDescriptor#Composite Score`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/AssessmentReportingMethodDescriptor#Scale Score`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/AssessmentReportingMethodDescriptor#Performance Level`
 
### resultDatatypeTypeDescriptor:
- **studentAssessments.jsont**: `uri://ed.sc.gov/ResultDatatypeTypeDescriptor#Decimal`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `uri://ed.sc.gov/ResultDatatypeTypeDescriptor#Integer`

### performanceLevelDescriptor:
- Here the namespace is :  `uri://avantassessment.com`
- **objectiveAssessments.jsont**: `{{namespace}}/PerformanceLevelDescriptor#{{PerformanceLevelDescriptor}}`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/PerformanceLevelDescriptor#{{Reading_Level}}, {{Writing_Level}}, {{Listening_Level}}, {{Speaking_Level}}`
- Here the performance level descriptors match the top level objectives: Reading, Writing, Listening and Speaking 
- **performanceLevelDescriptors.csv**: Novice-Low, Novice-Mid, Novice-High, Intermediate-Low, Intermediate-Mid, Intermediate-High, Advanced-Low, Advanced-Mid, Advanced-High, NS, IP, SP, NR 

### academicSubjectDescriptor:
- **assessments.jsont**: `uri://ed.sc.gov/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`
- **assessments.csv**: Language proficiency 
- **objectiveAssessments.jsont**: `uri://ed.sc.gov/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`
- **objectiveAssessments.csv**: Reading, Writing, Listening, Speaking 

### GradeLevelDescriptor:
- **assessments.jsont**: `uri://ed.sc.gov/GradeLevelDescriptor#{{assessedGradeLevelDescriptor}}`
- **studentAssessments.jsont**: `uri://ed.sc.gov/GradeLevelDescriptor#{{whenAssessedGradeLevelDescriptor}}`

### educationOrganizationAssociationTypeDescriptor:
- **educationOrganizationAssociationTypeDescriptor**: `uri://ed.sc.gov/EducationOrganizationAssociationTypeDescriptor#Attribution`

### languageDescriptor:
- **assessments.jsont**: `uri://ed.sc.gov/LanguageDescriptor#{{languageDescriptor}}`



