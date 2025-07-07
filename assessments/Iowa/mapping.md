# IOWA Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - IOWA-Survey
  - IOWA-Complete

## Assessment Family
IOWA

## Namespace
Namespace: uri://www.riversideinsights.com/Iowa_Assessments

# Objectives
## Objectives Identifiers
For each assessment there are the following objectives identifiers:
 - R: Reading
 - V: Vocabulary
 - SP: Spelling
 - CP: Capitalization
 - PC: Punctuation
 - L: Language (levels 05-08)
 - WE: Written Expression (levels 09-17) (in Appendix A layout definitions this objective doesn't have a slot number, DLP has used the same slot number for both WE and CW, which is incorrect for arrays in the template. )
 - CW: Conventions of Writing
 - ET: ELA Total
 - WA: Word Analysis
 - Li: Listening
 - XET: Extended ELA Total
 - M: Mathematics (or MT without Comp)
 - MC: Computation
 - MT: Math Total (with Comp)
 - CT: Core Composite (with ELA | with Comp)
 - XCT: Core Composite (with Extended ELA | with Comp)
 - CT-: Core Composite (with ELA without Comp)
 - XCT-: Core Composite (with Extended ELA without Comp)
 - SS: Social Studies
 - SC: Science
 - CC: Complete Composite (with ELA | with Comp)
 - XCC: Complete Composite (with Extended ELA | with Comp)
 - CC-: Complete Composite (with ELA without Comp)
 - XCC-: Complete Composite (with Extended ELA without Comp)
 - RW: Reading Words for Level 06 only (this is Reading Part 1 reported in Slot 1)
 - RC: Reading Comprehension for Level 06 only (this is Reading Part 2 reported in Slot 1)
 - RT: Reading Total
 - LT: Language Total
 - N/A: Not used
 - N/A-2: Not used

## Performance levels
 - 1 = Completion Criteria met 
 - 0 = Completion Criteria not met
 - -1 = Test not included in the Battery

## Assessments Score Method Descriptors
These are the score method descriptors:

The following scores are not tied to an objective, so I can assume that they are overall scores. (always empty)
 - Predicted SAT Critical Reading High (overall)
 - Predicted SAT Critical Reading Low (overall)
 - Predicted SAT Math High (overall)
 - Predicted SAT Math Low (overall)
 - Predicted ACT Composite High (overall)
 - Predicted ACT Composite Low (overall)

The following scores are tied to an objective, so they are objectives scores:
 - Number Attempted
 - Completion Criteria, modeled as Performance Level
 - Raw Score
 - Standard Score
 - Grade Equivalent
 - National Percentile Rank
 - National Curve Equivalent
 - National Stanine
 - Predicted Standard Score
 - Predicted Grade Equivalent
 - Predicted National Percentile Rank
 - Predicted Standard Score Diffs (Date format in sample file)
 - Predicted Grade Equivalent Diffs
 - Local Percentile Rank
 - Local Stanine
 - SDCD Levels Percent Correct
 - CSS Domain Percent Correct
 - College Readiness
 - Standard Score based on 2011 or 2005 norms 
   - Standard Score based on 2005 norms, if 'Norm Year'= 11
   - Standard Score based on 2011 norms, if 'Norm Year'= 17
 - Grade Equivalent based on 2005 or 2011 norms 
   - Grade Equivalent based on 2005 norms, if 'Norm Year'= 11
   - Grade Equivalent based on 2011 norms, if 'Norm Year'= 17
 - National Percentile Rank based on 2005 or 2011 norms 
   - National Percentile Rank based on 2005 norms, if 'Norm Year'= 11
   - National Percentile Rank based on 2011 norms, if 'Norm Year'= 17
 - National Stanine based on 2005 or 2011 norms 
   - National Stanine based on 2005 norms, if 'Norm Year'= 11
   - National Stanine based on 2011 norms, if 'Norm Year'= 17
 - CSS without Computation Domain Percent Correct
 - State Predicted Scale Score: Low Score of Range
 - State Predicted Scale Score: High Score of Range
 - State Predicted Scale Score
 - PR Valid Flag
 - Significant Diff Indicators
 - Filler / Catholic - Private PR
 - Filler / HSES PR
 - Filler / LSES PR
 
They have 2 records per student in studentAssessment for IOWA-Complete, that is not correct. It should be IOWA-Survey. 
 
# Hierarchy
![alt text](hierarchy.png)

## Reasoning




# Data Sources

## Input Requirements


## Bundle Seeds



## Summary of Descriptor Fields and Mappings


### gradeLevelDescriptor:
uri://ed-fi.org/GradeLevelDescriptor
- Kindergarten
- First grade
- Second grade
- Third grade
- Fourth grade
- Fifth grade
- Sixth grade
- Seventh grade
- Eighth grade
- Ninth grade
- Tenth grade
- Eleventh grade
- Twelfth grade
- Grade 13

### assessmentCategoryDescriptor:
- uri://www.riversideinsights.com/IowaAssessments/AssessmentCategoryDescriptor#Achievement Test

### assessmentReportingMethodDescriptor:
uri://www.riversideinsights.com/Iowa_Assessments/AssessmentReportingMethodDescriptor
- Number Attempted
- Completion Criteria
- Raw Score
- Standard Score
- Grade Equivalent
- National Percentile Rank
- National Curve Equivalent
- National Stanine
- Predicted Standard Score
- Predicted Grade Equivalent
- Predicted National Percentile Rank
- Predicted Standard Score Diffs
- Predicted Grade Equivalent Diffs
- Local Percentile Rank
- Local Stanine
- Predicted SAT Critical Reading High
- Predicted SAT Critical Reading Low
- Predicted SAT Math High
- Predicted SAT Math Low
- Predicted ACT Composite High
- Predicted ACT Composite Low
- SDCD Levels Percent Correct
- CSS Domain Percent Correct
- College Readiness
- Standard Score based on 2005 norms
- Standard Score based on 2011 norms
- Grade Equivalent based on 2005 norms
- Grade Equivalent based on 2011 norms
- National Percentile Rank based on 2005 norms
- National Percentile Rank based on 2011 norms
- National Stanine based on 2005 norms
- National Stanine based on 2011 norms
- CSS without Computation Domain Percent Correct
- State Predicted Scale Score: Low Score of Range
- State Predicted Scale Score: High Score of Range
- State Predicted Scale Score
- PR Valid Flag
- Significant Diff Indicators
- Catholic - Private PR
- HSES PR
- LSES PR


### accommodationDescriptors:
uri://www.riversideinsights.com/Iowa_Assessments/AccommodationDescriptor

  - Online desktop or laptop
  - Online tablet
  - Large Print
  - Proctor led
  - Self-paced
  - Audio Type
  - English Language Administration
  - Spanish Language Administration
  - Extended Time
  - Reserved for future
  - Braille

# Output Files

- accommodationDescriptors.jsonl
- assessmentCategoryMethodDescriptors.jsonl
- assessmentPeriodDescriptors.jsonl
- assessmentReportingMethodDescriptors.jsonl
- assessments.jsonl
- objectiveAssessments.jsonl
- studentAssessmentEducationOrganizationAssociations.jsonl
- studentAssessments.jsonl


- performanceLevelDescriptors.jsonl

# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:

