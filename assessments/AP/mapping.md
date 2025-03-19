# Assessment Details
STAMP stands for STAndards-based Measurement of Proficiency.  It is a language proficiency assessment aligned with the three major proficiency levels of Novice, Intermediate and Advanced (and their sub-levels) that are recognized by the American Council on the Teaching of Foreign Languages (ACTFL). The assessments are based on the ACTFL Proficiency Guidelines.
Avant provides a variety of assessments which tests variations of the four language skills: Reading, Writing, Listening, and Speaking.
Assessments are offered in all four skills (STAMP 4S) or a variation/combination of those skills including one, two, or three skills. These assess what an individual can do with language (reading, writing, listening, and speaking) in a sustained way in real-world contexts.

## Assessment
This bundle was designed for 5 types of STAMP test:
 - STAMP 4S
- STAMP WS
- STAMP Latin
- STAMP Monolingual
- STAMP ASL

## Assessment Family
- STAMP

## Assessment Identifier(s)
- There are five AssessmentIdentifiers based on the different STAMP tests.
    - STAMP 4S
    - STAMP WS
    - STAMP Latin
    - STAMP Monolingual
    - STAMP ASL
Logic to determine which language associates with which assessmentIdentifier for a test.
    - If the Language field = "Latin" then assessmentIdentifier = "STAMP Latin"
    - If the Language field = "Spanish Monolingual" then assessmentIdentifier = "STAMP Spanish Monolingual
    - If the Language field = "ASL" then assessmentIdentifier = "STAMP ASL”
    - If the Language field is not in ("Latin","Spanish Monolingual","ASL") AND only WritingBenchmark and SpeakingBenchmark fields are populated, then assessmentIdentifier = "STAMP WS"
    - else assessmentIdentifier = "STAMP 4S"

## Objective Assessment
The language skills tested are designated as objective assessments. These are also mapped as the academic subject area for the objective assessments. Each test has some combination of these four language skills, except for STAMP ASL:
- Reading
- Writing
- Listening
- Speaking
STAMP ASL assesses these two skills:
- Expressive
- Receptive
The other STAMP tests assess these specific skills:
- STAMP 4S
    - Reading
    - Writing
    - Listening
    - Speaking
- STAMP WS
    - Writing
    - Speaking
- STAMP Latin
    - Reading
- STAMP Monolingual
    - Writing
    - Speaking

## Assessment Language(s)
- There are several languages associated with the two test STAMP 4S and STAMP WS, the mappings for which are provided. 
- Note: Highlighted languages do not have a one to one mapping with the Ed-Fi language descriptor values. These will need to be verified and correct values added for your implementation if you are using the Ed-Fi language descriptor values.
   - American Sign Language mapped to sgn code value for Language Descriptor.
   - Arabic mapped to ara code value for Language Descriptor.
   - English mapped to eng code value for Language Descriptor.
   - French mapped to fre code value for Language Descriptor.
   - German mapped to ger code value for Language Descriptor.
   - Hebrew mapped to heb code value for Language Descriptor.
   - Hindi mapped to hin code value for Language Descriptor.
   - Italian mapped to ita code value for Language Descriptor.
   - Japanese mapped to jpn code value for Language Descriptor.
   - Korean mapped to kor code value for Language Descriptor.
   - Latin mapped to lat code value for Language Descriptor.
   - **Mandarin Simplified mapped to ace code value for Language Descriptor. (Achinese)**
   - **Mandarin Traditional mapped to chi code value for Language Descriptor. (Chinese)**
   - Polish mapped to pol code value for Language Descriptor.
   - Portuguese mapped to por code value for Language Descriptor.
   - Russian mapped to rus code value for Language Descriptor.
   - Spanish mapped to spa code value for Language Descriptor.
   - Spanish Monolingual mapped to spa code value for Language Descriptor.
   - Swahili mapped to swa code value for Language Descriptor.
   - Yoruba mapped to yor code value for Language Descriptor.
   - Amharic mapped to amh code value for Language Descriptor.
   - Armenian mapped to arm code value for Language Descriptor.
   - Bengali mapped to ben code value for Language Descriptor.
   - **Cabo Verdean mapped to ach code value for Language Descriptor. (Acoli)**
   - **Chaldean mapped to akk code value for Language Descriptor.(Akkadian)**
   - **Chin (Hakha) mapped to bur code value for Language Descriptor. (Burmese)**
   - Chuukese mapped to chk code value for Language Descriptor.
   - Czech mapped to cze code value for Language Descriptor.
   - Filipino(Tagalog) mapped to tgl code value for Language Descriptor.
   - Filipino mapped to fil code value for Language Descriptor.
   - Greek mapped to gre code value for Language Descriptor.
   - Haitian-Creole mapped to hat code value for Language Descriptor.
   - Hawaiian mapped to haw code value for Language Descriptor.
   - Hmong mapped to hmn code value for Language Descriptor.
   - **Ilocano mapped to ilo code value for Language Descriptor. (Iloko)**
   - Kannada mapped to kan code value for Language Descriptor.
   - Khmer mapped to khm code value for Language Descriptor.
   - Marshallese mapped to mah code value for Language Descriptor.
   - Marathi mapped to mar code value for Language Descriptor.
   - Nepali mapped to nep code value for Language Descriptor.
   - Pashto mapped to pus code value for Language Descriptor.
   - **Persian-Farsi mapped to per code value for Language Descriptor. (Persian)**
   - Pohnpeian mapped to pon code value for Language Descriptor.
   - Punjabi mapped to pan code value for Language Descriptor.
   - Romanian mapped to rum code value for Language Descriptor.
   - Samoan mapped to smo code value for Language Descriptor.
   - Somali Maay Maay mapped to som code value for Language Descriptor.
   - **Somali Maxaa mapped to mas code value for Language Descriptor. (Masai)**
   - Tamil mapped to tam code value for Language Descriptor.
   - Telugu mapped to tel code value for Language Descriptor.
   - Thai mapped to tha code value for Language Descriptor.
   - Tigrinya mapped to tir code value for Language Descriptor.
   - Turkish mapped to tur code value for Language Descriptor.
   - Ukrainian mapped to ukr code value for Language Descriptor.
   - Urdu mapped to urd code value for Language Descriptor.
   - Vietnamese mapped to vie code value for Language Descriptor.
   - Yup'ik mapped to ypk code value for Language Descriptor.
   - **Zomi mapped to ben code value for Language Descriptor. (Bengali)**

## Assessment Score
Test takers receive a composite score for the overall assessment. This is mapped accordingly.
Test Takers receive a scale score for reading and Listening skills. These are mapped accordingly.

## Assessment Score Assessment Reporting Method Descriptors
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Composite Score

## OnjectiveAssessment Score Assessment Reporting Method Descriptors
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Scale score
- uri://avantassessment.com/AssessmentReportingMethodDescriptor#Proficiency level

## Assessment Performance Levels
Test takers receive a benchmark score for each skill tested. Benchmark levels range from a value of 1 to 8 or 1 to 9 based on the skill being assessed.
- Reading and Listening 
    - 1 mapped to 1-Novice-Low
    - 2 mapped to 2-Novice-Mid
    - 3 mapped to 3-Novice-High
    - 4 mapped to Intermediate-Low
    - 5 mapped to Intermediate-Mid
    - 6 mapped to Intermediate-High
    - 7 mapped to Advanced-Low
    - 8 mapped to Advanced-Mid
    - 9 mapped to Advanced-High
- Writing and Speaking
    - 1 mapped to 1-Novice-Low
    - 2 mapped to 2-Novice-Mid
    - 3 mapped to 3-Novice-High
    - 4 mapped to Intermediate-Low
    - 5 mapped to Intermediate-Mid
    - 6 mapped to Intermediate-High
    - 7 mapped to Advanced-Low
    - 8 mapped to Advanced-Mid/High

# Hierarchy for Scores and Performance Levels
![alt text](image.png)

## Assessment Academic Subject Descriptor
- uri://ed-fi.org/AcademicSubjectDescriptor#Composite

## ObjectiveAssessment Academic Subject Descriptor
- uri://ed-fi.org/AcademicSubjectDescriptor#Reading
- uri://ed-fi.org/AcademicSubjectDescriptor#Writing
- uri://ed-fi.org/AcademicSubjectDescriptor#Critical Reading
- uri://ed-fi.org/AcademicSubjectDescriptor#Other
- The mapping for the Objectives to academic subject descriptor are identified below. 
- Note: Highlighted objectives do not have a one to one mapping with the Ed-Fi academic subject descriptors. These will need to be verified and correct values added for your implementation if you are using the Ed-Fi academic subject descriptors.
    - objective Reading mapped to academic subject descriptor Reading.
    - objective Writing mapped to academic subject descriptor Writing.
    - **objective Listening mapped to academic subject descriptor Critical Reading.**
    - **objective Speaking mapped to academic subject descriptor Other.**


## StudentAssessmentIdentifier
- This is derived by concatenating the assessmentIdentifier, test taker id and start date then hashing the value with md5. "assessmentIdentifier ~ '-' ~ studentUniqueId ~ '-' ~  StartDate"
- For example for Stamp 4S in the language Spanish taken by student with test taker id 9999 on date 12/1/2024, the StudentAssessmentIdentifier is the md5 hash of "STAMP 4S-Spanish-9999-12/1/2024".

## StudentAssessmentEducationOrganizationAssociation
- District is mapped for this entity with EducationOrganizationAssociation type of Attribution.

## SchoolYear
- The School Year is derived by taking the year portion of the Start Date. 
- If the month of the Start Date is >=7 then SchoolYear is the Year from the Start Date + 1 else SchoolYear is Year from the Start Date.
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
- **studentAssessments.jsont**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Decimal`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`

### performanceLevelDescriptor:
- Here the namespace is :  `uri://avantassessment.com`
- **objectiveAssessments.jsont**: `{{namespace}}/PerformanceLevelDescriptor#{{PerformanceLevelDescriptor}}`
- **studentAssessments.jsont (within studentObjectiveAssessments)**: `{{namespace}}/PerformanceLevelDescriptor#{{Reading_Level}}, {{Writing_Level}}, {{Listening_Level}}, {{Speaking_Level}}`
- Here the performance level descriptors match the top level objectives: Reading, Writing, Listening and Speaking 
- **performanceLevelDescriptors.csv**: Novice-Low, Novice-Mid, Novice-High, Intermediate-Low, Intermediate-Mid, Intermediate-High, Advanced-Low, Advanced-Mid, Advanced-High, NS, IP, SP, NR 

### academicSubjectDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`
- **assessments.csv**: Composite 
- **objectiveAssessments.jsont**: `uri://ed-fi.org/AcademicSubjectDescriptor#{{academicSubjectDescriptor}}`
- **objectiveAssessments.csv**: Reading, Writing, Critical Reading, Other 

### GradeLevelDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/GradeLevelDescriptor#{{assessedGradeLevelDescriptor}}`
- **studentAssessments.jsont**: `uri://ed-fi.org/GradeLevelDescriptor#{{whenAssessedGradeLevelDescriptor}}`

### educationOrganizationAssociationTypeDescriptor:
- **educationOrganizationAssociationTypeDescriptor**: `uri://ed-fi.org/EducationOrganizationAssociationTypeDescriptor#Attribution`

### languageDescriptor:
- **assessments.jsont**: `uri://ed-fi.org/LanguageDescriptor#{{languageDescriptor}}`
- **assessments.csv**:  American Sign Language, Arabic, English, French, German, Hebrew, Hindi, Italian, Japanese, Korean, Latin, Mandarin Simplified, Mandarin Traditional, Pohnpeia, Polish, Portuguese, Romanian, Russian, Spanish, Spanish Monolingual, Swahili, Yoruba, Amharic, Armenian, Bengali, Cabo Verdean, Chaldean,Chin (Hakha), Chuukese, Czech, Filipino, Filipino (Tagalog), Greek, Haitian-Creole, Hawaiian, Hmong, Ilocano, Kannada, Khmer, Marshallese, Marathi, Nepali, Pashto, Persian-Farsi, Punjabi, Samoan, Somali Maay Maay, Somali Maxaa, Tamil, Telugu, Thai, Tigrinya, Turkish, Ukrainian, Urdu, Vietnamese, Yup’ik, Zomi