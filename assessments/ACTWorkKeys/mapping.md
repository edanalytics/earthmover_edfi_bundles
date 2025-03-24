# ACTWorkKeys Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
- Each ACTWorkKeys assessment component is mapped to a unique Assessment file.
- Assessment Identifiers:
  - Workkeys_AM: Applied Mathematics
  - Workkeys_LI: Locating Information
  - Workkeys_RI: Reading for Information

## Assessment Family
ACT

## Assessments Score Method Descriptors
For each assessment there will be two score method descriptors:
 - Level Score
 - Scale Score
  
  
# Hierarchy
![alt text](hierarchy.png)

## Reasoning
The ACT WorkKeys Assessment is administered to measure foundational career readiness skills that are essential across a wide range of occupations. The purpose of this assessment is to evaluate students' applied knowledge in real-world scenarios.

This assessment supports instructional and accountability goals by providing reliable, standardized data that informs educational planning, workforce alignment, and credentialing decisions. The results can be used to help students identify career pathways, assist educators in tailoring instruction, and help employers evaluate workforce preparedness.

This bundle processes ACT WorkKeys assessment data, transforming it into Ed-Fi compatible assessment and student assessment records. The bundle handles multiple ACTWorkKeys assessments including Applied Mathematics, Locating Information, and Reading for Information. (There are differences between the name of the assessments on the ACT website and the documentation provided. The website displays 3 types of assessments with these names: Applied Math, Workplace Documents and Graphic Literacy. Which are the correct ones?)

# Data Sources

## Input Requirements
- Primary source file containing student ACTWorkKeys assessment data with the following required columns:
  - stateid: student unique identifier.
  - testdate: Assessment administration date
  - Assessment scores:
    - mathlevc: Applied Mathematics Level Score 
    - mathssc: Applied Mathematics Scale Score
    - infolevc: Locating Information Level Score
    - infossc: Locating Information Scale Score
    - readlevc: Reading for Information Level Score
    - readssc: Reading for Information Scale Score

## Bundle Seeds
- assessments.csv: Contains assessment metadata
- assessmentReportingMethodDescriptors.csv: Contains assessment reporting methods
- assessmentCategoryDescriptors.csv: Contains category descriptors
- gradeLevelDescriptors.csv: Contains grade level descriptors

# Ed-Fi Mapping
This bundle produces the following Ed-Fi resources:


## StudentAssessments
- studentAssessmentIdentifier: Generated using MD5 hash of assessmentIdentifier, studentUniqueId, and assessment date
- administrationDate: Mapped from testdate
- schoolYear: Mapped from testdate
- studentReference: Mapped from stateid
- scoreResults:
  - assessmentReportingMethodDescriptor: Mapped from descriptor source
  - resultDatatypeTypeDescriptor: Set to "Integer"
  - result: Mapped from corresponding assessment score column

## Summary of Descriptor Fields and Mappings

### academicSubjectDescriptor:
- Mathematics: **Namespace**: `uri://ed.sc.gov/AcademicSubjectDescriptor#Mathematics`
- Graphic Literacy: **Namespace**:   ???
- Language Arts: **Namespace**: `uri://ed.sc.gov/AcademicSubjectDescriptor#Language Arts`

### gradeLevelDescriptor: 
The documentation has 2 columns regarding education level. edlevP if source is WKPP
edlevO if sourse is WKIV with these possible vales:
- edlevP, level of education when testing method is WKPP. Should be one of them: 
  - 1 = 7th Grade
  - 2 = 8th Grade   
  - 3 = 9th Grade   
  - 4 = 10th Grade  
  - 5 = 11th Grade  
  - 6 = 12th Grade
  - 7 = H.S. Grad.
  - 8 = GED
  - 9 = Other Secondary
  - 10 = 1st Year Postsecondary
  - 11 = 2nd Year Postsecondary
  - 12 = 3rd Year Postsecondary
  - 13 = 4th Year Postsecondary
  - 14 = 5th Year or Higher Post.
  - 15 = Other Postsecondary
  
  
- edlevO, level of education when testing method is WKIV. Should be one of them: 
  - 8th Grade or below
  - 9th Grade
  - 10th Grade
  - 11th Grade
  - 12th Grade
  - Dual enrollment-11th grade & college
  - Dual enrollment-12th grade & college
  - Trade/Proprietary school
  - Community College
  - Postsecondary-4-Year Institutions: Freshman
  - Postsecondary-4-Year Institutions: Sophomore
  - Postsecondary-4-Year Institutions: Junior
  - Postsecondary-4-Year Institutions: Senior
  - Postsecondary-4-Year Institutions: Postgraduate

It will need a crosswalk file to map them.


### assessmentCategoryDescriptor:
- **Namespace**: `uri://ed.sc.gov/AssessmentCategoryDescriptor#HS_CAREER_COLLEGE`

### assessmentReportingMethodDescriptor:
- **Namespace**: `uri://ed.sc.gov/AssessmentReportingMethodDescriptor#Scale Score`
- **Namespace**: `uri://ed.sc.gov/AssessmentReportingMethodDescriptor#Level Score`

### resultDatatypeTypeDescriptor:
- **Namespace**: `uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer`


# Transformations

## Assessments:
Prepares assessment metadata by joining assessment information with grade level and reporting method descriptors.

## Students Assessments:
Three parallel transformations, one for each ACTWorkkeys assessment component:
- student_assessment_am
- student_assessment_li
- student_assessment_ri

Each transformation:
1. Adds specific assessmentIdentifier
2. Maps student identifiers
3. Adds assessment administration metadata
4. Generates unique studentAssessmentIdentifier
5. Joins with reporting method descriptors
6. Creates score JSON structure

All of them combined in one output file.

# Output Files

- assessmentReportingMethodDescriptors.jsonl
- assessmentCategoryMethodDescriptors.jsonl
- assessments.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- student_assessments.jsonl

# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:
  - ./templates/assessments.jsont
  - ./templates/assessmentReportingMethodDescriptors.jsont
  - ./templates/assessmentCategoryDescriptors.jsont
  - ./templates/descriptors.jsont
  - ./templates/studentAssessments.jsont
  - ./templates/studentAssessmentEducationOrganizationAssociations.jsont

