# IOWA Assessment Bundle Documentation

# Assessments
## Assessments Identifiers
  - IOWA-Survey
  - IOWA-Complete

## Assessment Family
IOWA

## Namespace
DLP uses DESCRIPTOR_NAMESPACE_OVERRIDE=uri://ed-fi.org/ as default for all the elements and sends as parameter any descriptor to replace with. 
So, I think we can fix it by replacing the namespace for assessment, objectiveAssessment, performanceLevelDescriptors, assessmentCategoryDescriptor, assessmentReportingMethodDescriptor, assessmentPeriodDescriptor, accommodationDescriptors.

Possible namespace: uri://www.riversideinsights.com/Iowa

# Objectives
## Objectives Identifiers
For each assessment there are these objectives identifiers:
 - R: Reading
 - V: Vocabulary
 - SP: Spelling
 - CP: Capitalization
 - PC: Punctuation
 - L: Language (levels 05-08)
 - WE: Written Expression (levels 09-17)
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
There are these score method descriptors:

The following scores are not tied to an objective, so I can assume that they are overall scores
 - Predicted SAT Critical Reading High (overall)
 - Predicted SAT Critical Reading Low (overall)
 - Predicted SAT Math High (overall)
 - Predicted SAT Math Low (overall)
 - Predicted ACT Composite High (overall)
 - Predicted ACT Composite Low (overall)

The following scores are tied to an objective, so they are objectives scores
 - Number Attempted
 - Completion Criteria, also modeled as Performance Level
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
 

 
# Hierarchy
![alt text](hierarchy.png)

## Reasoning




# Data Sources

## Input Requirements


## Bundle Seeds



# Ed-Fi Mapping
This bundle produces the following Ed-Fi resources:


## StudentAssessments


## Summary of Descriptor Fields and Mappings


### gradeLevelDescriptor:
- Namespace: `uri://ed-fi.org/GradeLevelDescriptor`


### assessmentCategoryDescriptor:


### assessmentReportingMethodDescriptor:

### resultDatatypeTypeDescriptor:

### assessmentPlatformTypeDescriptors:

### accommodationDescriptors:
  - Online desktop or laptop
  - Online tablet
  - Large Print
  - Proctor led
  - Self-paced
  - Audio Type
  - English Language Administration
  - Spanish Language Administration
  - Extended Time

# Output Files



# Dependencies
- Requires Earthmover version 0.3.8 or higher
- Requires template files:

