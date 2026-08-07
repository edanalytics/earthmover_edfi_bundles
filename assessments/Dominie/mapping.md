# Dominie Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
 - Dominie_General_Show Me Book
 - Dominie_General_Name Writing
 - Dominie_General_Letter Know
 - Dominie_General_Phoneme Segmentation
 - Dominie_General_Phoneme Deletion
 - Dominie_General_Core Rdg.
 - Dominie_General_Core Wtg. Vocab.
 - Dominie_General_Non. Fic. Show Me Book
 - Dominie_Sentence Writing & Spelling_Phonemes
 - Dominie_Sentence Writing & Spelling_Spelling
 - Dominie_Text Reading_Benchmark or Bridge Level
 - Dominie_Text Reading_Equated Level
 - Dominie_Text Reading_ACC%
 - Dominie_Text Reading_Self Correction Rate
 - Dominie_Text Reading_WCPM
 - Dominie_Text Reading_Fluency Rubric
 - Dominie_Text Reading_COMP%
 - Dominie_Text Reading_% Meaning
 - Dominie_Text Reading_% Visual
 - Dominie_Phonics / Forms A & B_Onsets
 - Dominie_Phonics / Forms A & B_Rimes
 - Dominie_Story Writing_Conventions
 - Dominie_Story Writing_Message
 - Dominie_Spelling Inventory_Spelling Inventory


## Assessment Family
Dominie

## Assessments Score Method Descriptors
Each assessment corresponds to a particular literacy skill. When multiple scoring methods are available for the same skill, such as a raw score and a stanine score, they are represented as separate score entries under the same assessment.

This assessment has the following Reporting Method Descriptors:
 - Raw Score: string
 - Percent: decimal
 - Stanine: Standard nine-point scale scores for norm-referenced interpretation (integer)
 - Rubric: decimal

# Hierarchy
![alt text](hierarchy.png)

## Reasoning
The Dominie Reading and Writing Assessment is designed to provide a comprehensive, formative evaluation of early literacy skills for students in kindergarten through third grade. Its purpose is to guide instruction and intervention by assessing foundational components of reading and writing, including phonemic awareness, phonics, fluency, comprehension, vocabulary, spelling, and writing conventions. The assessment’s portfolio-based format allows educators to capture individual student progress across multiple domains, inform instructional decisions, and support differentiated learning based on student needs.

# Data Sources

## Input Requirements
- Primary source file containing student Dominie assessment data with the following required columns:
  - Student unique identifier.
  - Assessment administration date
  - Assessment identifier
  - Scores.


## Bundle Seeds
- `assessments.csv`: Contains assessment metadata
- `assessmentReportingMethodDescriptors.csv`: Contains assessment reporting methods
- `assessmentCategoryDescriptors.csv`: Contains category descriptors
- `gradeLevelMapping.csv`: Grade level values by testing type


# Ed-Fi Mapping
This bundle produces the following Ed-Fi resources:


## StudentAssessments
- studentAssessmentIdentifier: Generated using MD5 hash of assessmentIdentifier, studentUniqueId, and assessment date
- administrationDate: Mapped from datetaken
- schoolYear: Mapped from datetaken
- studentReference: Mapped from suns
- scoreResults:
  - assessmentReportingMethodDescriptor: Mapped from descriptor source
  - resultDatatypeTypeDescriptor
  - result: Mapped from corresponding objective assessment score column

## Summary of Descriptor Fields and Mappings


### gradeLevelDescriptor:
- Namespace: `uri://ed-fi.org/GradeLevelDescriptor`

### assessmentCategoryDescriptor:
- `uri://pearson.com/AssessmentCategoryDescriptor#Diagnostic`

### assessmentReportingMethodDescriptor:
 - Raw Score: `uri://pearson.com/AssessmentReportingMethodDescriptor#Raw Score`
 - Percent: `uri://pearson.com/AssessmentReportingMethodDescriptor#Percent`
 - Stanine: `uri://pearson.com/AssessmentReportingMethodDescriptor#Stanine`
 - Rubric: `uri://pearson.com/AssessmentReportingMethodDescriptor#Rubric`


# Output Files

- assessmentReportingMethodDescriptors.jsonl
- assessments.jsonl
- assessmentCategoryDescriptors.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl

# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:
  - ./templates/assessments.jsont
  - ./templates/descriptors.jsont
  - ./templates/studentAssessments.jsont
  - ./templates/studentAssessmentEducationOrganizationAssociations.jsont

