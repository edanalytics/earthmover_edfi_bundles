* **Title**: Wisconsin Forward Exam
* **Description**: This maps the state assessment for Wisconsin, the Forward Exam, administered in ELA, mathematics, science, and social studies.
* **Submitter name**: Alex Chen
* **Submitter organization**: Education Analytics

## Model

Data model is based on information in the [User's Guide to Interpreting Reports 2024-25](https://dpi.wi.gov/sites/default/files/imce/assessment/pdf/Forward_Exam_Users_Guide_to_Interpreting_Reports_2024-25.pdf) as well as the [Wisconsin Forward Exam Spring 2024 Technical Report](https://dpi.wi.gov/sites/default/files/imce/assessment/pdf/Final_Forward_Technical_Report_2024.pdf) for 2023-2025. For historical data, information was sourced from:
- For 2022-23, the [2023 Technical Report](https://dpi.wi.gov/sites/default/files/imce/assessment/pdf/EWI270_WIFW_SPRG_23_TECH.pdf) covers the content standards and different scores, especially for major column name and score differences prior to changes in 2024.
- For 2021-22, the [Spring 2022 Technical Report](https://dpi.wi.gov/sites/default/files/imce/assessment/pdf/2022_Technical_Report_Final.pdf) includes past reporting categories and the old Listening domain for ELA, as well as mappings of letter codes to reporting categories to interpret column names.
- For 2020-21, the [2021 Technical Report](https://www.wistatedocuments.org/digital/collection/p267601coll4/id/34743/) covers past column names, especially for SS prior to renaming that occurred in 2021-22.
- For 2017-18, the [2018 Technical Report](https://dpi.state.wi.us/sites/default/files/imce/assessment/pdf/Forward_Exam_Tech_Report_2018.pdf) covers historical content standards and scores, especially for 
storical SCN objective assessments and scores prior to the 2019 update.  

Namespace is `uri://datarecognitioncorp.com` due to the underlying vendor.

### Assessments
Split into four by academic subject; TBD on whether official integration will split by grade as well:
- WIForward_ELA: English Language Arts 
- WIForward_MTH: Mathematics
- WIForward_SCN: Science
- WIForward_SS: Social Studies

For each of the subjects, the following scores/PLs are available:
- Scale score (can be "compared for individual students and groups in a given grade and content area" and "over time for all.. content areas for which the assessment scores are reported on the same year-to-year scale")
	- ELA, math retooled in 2024;
        - "Scale scores for ELA and mathematics for 2023-24 cannot be directly compared to prior years" according to a DPI [press release](https://dpi.wi.gov/news/releases/2024/student-assessment-results-forward). 
	- Science scale same since 2019, social studies scale same since 2022
- Scale score standard error
- Performance level, 1-4/Developing-Advanced, based on scale score (different cuts by grade and by subject)
    - This is called 'Proficiency' in 2022-23 and prior but is also a four-category performance level. The categories then are called 'Below Basic', 'Basic', 'Proficient', and 'Advanced'
    - Despite differences in level naming, both performance level and proficiency are only mapped to values 1-4 in the output of the bundle.
- WI percentile
- [WI Normal Curve Equivalent (NCE)](https://dpi.wi.gov/sites/default/files/imce/assessment/pdf/Percentile_Rank_Vs_Normal_Curve_Equivalent.pdf), prior to 2024

### Objective assessments

#### Domains
ELA is the only assessment split into domains, 1) Reading and 2) Writing/Language. Each of these has, like the top-level assessments, starting in 2024:
- Scale score
- Scale score standard error 
- Performance level, 1-4
- WI percentile

Prior to revisions in 2023-24, there was an additional Listening domain and scores/performance levels were as follows:
- Standard performance index (SPI) score
- SPI performance levels based on SPI scores


#### Reporting categories / content standards
Separate from domains, Forward also provides raw points, scale scores, and performance levels for each of the following reporting categories. Each category is targeted at specific knowledge areas, skills, or concepts. These differ by subject and can differ by grade for certain subjects. From 2023-24 onwards, scale scores are called 'Progress Scores' and the derived performance levels 'Progress Levels'. Prior, these were 'SPI (Standard Performance Index) Scores' and 'SPI Levels'; SPIs were also provided with upper and lower bounds.

ELA:
- Reading
	- Key Ideas and Details
	- Craft and Structure/Integration of Knowledge
	- Vocabulary Use
- Written/Language
	- Text Types and Purposes
	- Inquiry to Build and Present Knowledge (starting in 2023-24)
	- Language Conventions
    - Research (prior to 2023-24)

Math:
- Operations and Algebraic Thinking (grades 3-5)
- Number and Operations in Base Ten (grades 3-5)
- Number and Operations - Fractions (grades 3-5)
- Measurement and Data (grades 3-5)
- Geometry (grades 3-8)
- Ratios and Proportional Relationships (grades 6-7)
- The Number System (grades 6-8)
- Expressions and Equations (grades 6-8)
- Statistics and Probability (grades 6-8)
- Functions (grades 8)

Social Studies: (same for all grades)
- Behavioral Sciences
- Economics
- Geography
- History
- Political Science and Citizenship

Science (same for all grades, prefixed by 'Practices and Crosscutting Concepts in' from 2024 onwards):
- Life Science
- Physical Science
- Earth and Space Science
- Engineering (starting in 2019)
- Science Connections and Nature of Science (prior to 2019)
- Science Inquiry (prior to 2019)
- Science Applications and Personal Social Perspectives (prior to 2019)


### Accommodations and supports
Accommodations and supports are included, with mappings documented in `seeds/columns_to_accommodations.csv`. These are currently intended to best match the 2024-25 version of the assessment, with historical accommodations aligned where possible. There are some subject-specific accommodations, such as Read Aloud Passages or Listening Scripts for ELA or Multiplication Table for MTH.

## General bundle info
This bundle follows our current best-practices, which include:
- Implementing our Student ID Xwalking logic. To learn more about our student ID xwalk feature, see this [README](https://github.com/edanalytics/earthmover_edfi_bundles/tree/student_id_alignment/packages/student_ids). The student ID xwalking section below includes more information about imeplementing this feature in production. 
- Containing all default Ed-Fi descriptors (except for dataTypeDescriptors) in seed files, and never hard-coding those values in the templates. This allows an implementation to override those using [project composition](https://github.com/edanalytics/earthmover?tab=readme-ov-file#project-composition) in cases where the destination uses custom descriptors. This is typically true for gradeLevelDescriptors and academicSubjectDescriptors. 
- Including an **ANONYMIZED** sample file in the `data` folder. **DO NOT push real student data (PII) to GitHub**.
- Mapping the assessment following [Ed-Fi Assessment Data Governance best practices](https://edanalytics.slite.page/p/FwwhB84DoYVjY1/NEW-Assessment-Data-Governance-in-Ed-Fi).
- Including a `_metadata.yaml` file for Runway compatibility.
- Including a single `earthmover.yaml` file. If multiple are created to simplify code, one `earthmover.yaml` file should unify them, parameterized as necessary.
- Writing an in-depth README.
- Following minor consistency rules:
    + Not including the vendor of the assessment into the assessment identifier.
    + Not including the vendor of the assessment in the folder name of this bundle.
    + Ending the earthmover and lightbeam config files with `.yaml` instead of `.yml`.
    + Using relative paths.

This bundle has an experimental format where a large nested Python object (imported in Jinja via `from 'templates/assessment_structure.jinja' import assessments`) powers Jinja-driven operations in both `earthmover.yaml` and `studentAssessments.jsont`. Because there are substantive differences in objective assessments, scores, PLs, and accommodations over time, this object contains column-to-field mappings in a way that reflects the nested structure of `studentAssessment` records and captures the years for which mappings are active. This replaces the arrays of possible scores and PLs at the top of the studentAssessment template. The structure of the overall array looks something like the following:

```json
[
  {
    "assessmentIdentifier": "WIForward_ELA",
    "scoreResults": [
      {"reportingMethod": "Scale Score", "col": "scaleScore", "raw_col": "Scale_Score_ELA", "min_year": 2016, "max_year": 2100, "typeDescriptor": "Integer"},
      ...
    ],
    "performanceLevels": [
      {"reportingMethod": "Performance Level", "col": "performanceLevel", "raw_col": "ELA_Performance_Level", "min_year": 2024, "max_year": 2100, "levels": [1, 2, 3, 4]},
      ...
    ],
    "objectiveAssessments": [
      {
        "identificationCode": "Reading",
        "scoreResults": [
          {"reportingMethod": "Scale Score", "col": "Scale_Score_Reading", "min_year": 2024, "max_year": 2100, "typeDescriptor": "Integer"},
          ...
        ],
        "performanceLevels": [
          {"reportingMethod": "Performance Level", "col": "Reading_Performance_Level", "min_year": 2024, "max_year": 2100, "levels": [1, 2, 3, 4]},
          ...
        ]
      },
      ...
    ]
  },
  ...
]
```

Each field mapping is currently structured with the following entries:
- `reportingMethod` contains the value for the `assessmentReportingMethodDescriptor`
- `col` contains the column name to map to the final value; in some cases, for top-level assessment fields that stay the same across assessments, like scale scores present for all four subjects, this represents a column created in earthmover. In other cases, for objective assessment fields, this just reflects the raw column name in the original flat file.
- `raw_col` contains, if the raw column is mapped to a standard column name in earthmover, as with top-level subject scale scores, the original raw column name to map from.
- `min_year` and `max_year` contain the year limits of a column-to-field mapping, inclusive. A mapping valid from the 2023-24 school year onwards, for example, would have `min_year` of 2024 and a `max_year` of 2100 (this is an empty string in the seed file, but is filled with an arbitrarily high value in earthmover). 
- `levels` contains the possible levels for a performance level mapping, currently only used in the `assessments` and `objectiveAssessments` templates.

The object itself is in source control in `templates/assessment_structure.jinja`. For convenience in editing this object in the future, mappings are stored in tabular form in seeds, and the assessment structure object can be reconstructed by earthmover itself and output to `output/assessment_spec.jinja`. 

## Running this bundle without Student ID Xwalking
To run this bundle without implementing the student ID xwalking packages:
```bash
earthmover run -c ./earthmover.yaml -p '{
"STATE_FILE": "./runs.csv",
"INPUT_FILE": "data/sample_anonymized_file.csv",
"OUTPUT_DIR": "output/" ,
"STUDENT_ID_NAME": "WISEID",
"EDFI_DS_VERSION": "5",
"API_YEAR": 2025
}'
```

## Lightbeam
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```

## DAG Graph
![DAG view of transformations](graph.png)

(**Above**: a graphical depiction of the dataflow.)
