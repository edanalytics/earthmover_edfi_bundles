* **Title**: Washington Comprehensive Assessment of Science (WCAS)
* **Description**: This template includes the WCAS assessments, designed to measures the level of proficiency that Washington students have based on the Next Generation Science Standards (NGSS). It's given in **grades 5, 8, and 11** to meet the ESSA science testing requirement.
* **Submitter name**: Markisha Berrien-Fitzsimons
* **Submitter organization**: Education Analytics

---

## 1. The assessment

The WCAS is a **fixed-form** test. Every student in a grade sees the same items in the same order in a given year. 


## 2. Scores in the file

### Overall: scale score + performance level

| Grade | Level 1 | Level 2 | Level 3 | Level 4 | Full range |
|---|---|---|---|---|---|
| 5 | 375–649 | 650–699 | 700–784 | 785–1060 | **375–1060** |
| 8 | 345–649 | 650–699 | 700–764 | 765–1060 | **345–1060** |
| 11 | 390–649 | 650–699 | 700–790 | 791–1190 | **390–1190** |

<sub>Source: [OSPI — Scale Scores for State Assessments](https://ospi.k12.wa.us/student-success/testing/state-testing/state-testing-scores-and-reports/scale-scores-state-assessments)</sub>

Level meanings: L4 consistently demonstrates *advanced* grade-level knowledge and skills; L3
consistently demonstrates *proficient*; L2 demonstrates *foundational*; L1 does not consistently
demonstrate grade-level knowledge and skills.

<sub>Source: [OSPI — WCAS Sample Score Report](https://ospi.k12.wa.us/sites/default/files/2025-04/wcas-sample-score-report.PDF)</sub>

### Reporting areas: percent + band

Three areas:

1. Practices & Crosscutting Concepts in **Life Sciences**
2. Practices & Crosscutting Concepts in **Physical Sciences**
3. Practices & Crosscutting Concepts in **Earth & Space Sciences**

Each gives you a **percent points earned** (0–100) and a **band** (Below / At / Above Standard).

<sub>Source: [OSPI — WCAS Sample Score Report](https://ospi.k12.wa.us/sites/default/files/2025-04/wcas-sample-score-report.PDF)</sub>



**There is no Engineering/ETS area.** ETS performance expectations are bundled into clusters
belonging to one of the three reported domains, and ETS points are not separately specified.

<sub>Source: [OSPI — WCAS Test Design & Item Specs, Grade 5](https://ospi.k12.wa.us/sites/default/files/2026-04/grade-5-item-specs.pdf)</sub>

---

## 3. Things to watch out for

### 3.1 The reporting area denominator changes from year to year

The test design specifications sets the total number of points, but the split across areas can vary:

| Grade | Total | Physical | Life | Earth & Space |
|---|---|---|---|---|
| 5 | 35 | 12–16 | 8–12 | 9–13 |
| 8 | 40 | 12–16 | 13–17 | 9–13 |
| 11 | 45 | 14–18 | 14–18 | 11–15 |

<sub>Sources: OSPI — WCAS Test Design & Item Specifications,
[Grade 5](https://ospi.k12.wa.us/sites/default/files/2026-04/grade-5-item-specs.pdf)·
[Grade 8](https://ospi.k12.wa.us/sites/default/files/2026-04/grade-8-item-spec.pdf)·
[High School](https://ospi.k12.wa.us/sites/default/files/2026-04/hs-item-specs.pdf)</sub>

These are **points available**, not points earned. For example, Physical Sciences could be worth 14 points one year and 16 the next.

<sub>Source: [OSPI — WCAS Test Design & Item Specs, Grade 5](https://ospi.k12.wa.us/sites/default/files/2026-04/grade-5-item-specs.pdf)</sub>

### 3.2 Below/At/Above Standard has no fixed cut

The bands are set separately for each grade, year, and area, and the Office of Superintendent of Public Instruction (OSPI) doesn't publish the cut points.

The At Standard range for an area is based on how students who scored **Level 3 overall** performed in that area. In other words, "At Standard in Physical Sciences" means the student did about as well in Physical Sciences as students who met standard on the whole test.

<sub>Sources: [OSPI — WCAS Sample Score Report](https://ospi.k12.wa.us/sites/default/files/2025-04/wcas-sample-score-report.PDF) ·
[OSPI — WCAS FAQ](https://ospi.k12.wa.us/sites/default/files/2023-08/wcas_faq_2022_combined.pdf)</sub>

### 3.3 Overall and area results won't always line up

Both come from the same student responses. Every point belongs to exactly one area, and the area points add up to the total. However, the scale score is a transformation of all the points, while the area percents are simple raw percentages. **The scale score is not an average of the three area percents.**

---

## 4. Sample File Columns and Definitions

This file is exported from the Cambium **Centralized Reporting System**.

| Column | Type | Expected values | Notes |
|---|---|---|---|
| `Student ID` | string | N/A | N/A |
| `Student DOB` | date | N/A | N/A |
| `Test Reason` | string | One value per file | For summative tests, the test reason is the test window (e.g. `Spring 2025`). |
| `Test OppNumber` | N/A | N/A | An opportunity is one instance of a student taking the test. |
| `Date Taken` | date | N/A | Date the student started the test. |
| `Test Completion Date` | date | On or after `Date Taken` | Date the student submitted the test. |
| `Test Duration (Minutes)` | integer | 0 to several hundred | Total testing time. |

<sub>Sources: test reason & opportunity definitions and export options:
[Cambium — Reporting System User Guide 2026–27](https://www.oregon.gov/ode/educator-resources/assessment/Documents/osas_reports_userguide.pdf)</sub>

### Overall test results

| Column | Type | Expected values | Notes |
|---|---|---|---|
| `Grade N WCAS Summative Scale Score` | integer | Varies by grade | These ranges are hard limits, so any value outside them is an error. May be blank for invalidated or non-scorable tests. |
| `Grade N WCAS Summative Performance` | integer or string | `1` to `4` | Should match the scale score based on the cut score table. |

### Reporting areas

Each of the three areas has two columns.

| Column | Type | Expected values | Notes |
|---|---|---|---|
| `N. <area> Reporting Area Percent Points Earned` | integer | `0` to `100` | Points earned in the area divided by points available in the area, as a whole-number percentage. |
| `N. <area> Reporting Area Proficiency` | string | `Below Standard` / `At Standard` / `Above Standard` | Cut points are set separately for each grade, year, and area and are not published.  |

---

## 5. How this bundle maps the data

### 5.1 Assessments

The bundle creates one assessment resource. WCAS covers a single subject, so it is not split by subject the way the SBAC bundle is.

| Assessment identifier | Subject | Assessed grades |
| --- | --- | --- |
| `WCAS` | Science | 5, 8, 11 |

The assessment family is `WCAS`, the assessment category is **State summative assessment**, and all bundle-defined resources and descriptors use the namespace `uri://cambiumassessment.com`.

The namespace is defined once, in `seeds/assessments.csv`. Student assessment records pick it up through a join, so changing it there changes it for student records too. The other seeds that contain a namespace must be updated to match.

### 5.2 Student assessment results

For each student assessment, the bundle maps:

- **Summative Scale Score**
- **Performance Level** (`1`–`4`)
- **Grade when assessed** (first attempts only; see 5.4)
- **Administration date** (from `Date Taken`)
- **School year** (from `Test Reason`)
- **Retest indicator**

The source performance column may contain either `Level 3` or `3`. The bundle strips a leading `Level ` so both map to the same descriptor.

**Assessment Grade Level is intentionally not mapped.** WCAS retake files do not provide the data needed to distinguish the student's grade from the assessment's grade, so the bundle does not emit an assessment-grade score.

### 5.3 Objective assessments

Each reporting area (see section 2) is represented as an Ed-Fi `ObjectiveAssessment` / `StudentObjectiveAssessment`:

| identificationCode | Reporting area |
| --- | --- |
| `life_sciences` | 1. Practices & Crosscutting Concepts in Life Sciences |
| `physical_sciences` | 2. Practices & Crosscutting Concepts in Physical Sciences |
| `earth_space_sciences` | 3. Practices & Crosscutting Concepts in Earth & Space Sciences |

Each reporting area carries two results:

| Result | Ed-Fi representation | Values |
| --- | --- | --- |
| Percent Points Earned | `scoreResult` (datatype `Percentage`) | Passed through exactly as in the source, including a `%` sign if present (e.g. `30%`) |
| Reporting Area Proficiency | `performanceLevel` | `Above Standard`, `At Standard`, `Below Standard`, `Insufficient to score` |

A reporting area with no values (blank or `N/A`) is omitted from the student record.

### 5.4 Retakes

Retake files mark the score columns with `(RETAKE)`:

```text
Grade 11 WCAS Summative (RETAKE) Scale Score
Grade 11 WCAS Summative (RETAKE) Performance
```

From this the bundle sets the Ed-Fi `retestIndicatorDescriptor` to `True`, so retake status is preserved downstream.

Unlike the SBAC extracts, WCAS retake headers do **not** state the student's enrolled grade at the time of the retake. The bundle therefore **omits `whenAssessedGradeLevelDescriptor` for retakes** rather than guessing. For first attempts, the grade when assessed is taken to be the assessment's grade.

If a future extract includes the student's enrolled grade, `enrolled_grade` in `earthmover.yaml` is the place to use it.

### 5.5 Insufficient to score

Students who could not be scored have `Insufficient to score` in every score column. For these students:

- the scale score and Percent Points Earned are **omitted**, because they are not numbers;
- the overall performance level and each reporting-area proficiency are set to the **`Insufficient to score`** performance level descriptor.

The student record is still loaded, and the could-not-score status is stored rather than dropped.

---

## 6. Expected source structure

Section 4 describes the columns. This section covers what the bundle's parsing depends on.

The bundle reads the assessment grade and retake status from the **scale-score column name**, which must match this pattern:

```text
Grade 5 WCAS Summative Scale Score
Grade 8 WCAS Summative Scale Score
Grade 11 WCAS Summative Scale Score
Grade 11 WCAS Summative (RETAKE) Scale Score
```

The performance column follows the same pattern, ending in `Performance` instead of `Scale Score`.

Other parsing assumptions:

| Field | Format the bundle expects | Used for |
| --- | --- | --- |
| `Student ID` (or the column named by `STUDENT_ID_NAME`) | any | `studentUniqueId` |
| `Date Taken` | `MM/DD/YYYY` | `administrationDate` and the student assessment identifier |
| `Test Reason` | `Spring 2025-2026 (...)` | `schoolYear`, taken as the end year of the second word |

`Test Reason` must contain the full `YYYY-YYYY` school year as its second word, as in the sample files (`Spring 2025-2026 (WCAS Summative)`). A shorter value such as `Spring 2025` would produce the wrong school year.

After snake-casing, the reporting-area column names begin with a digit, which Jinja cannot use as a variable name. `rename_columns` in `earthmover.yaml` maps each one to a short name (e.g. `life_sciences_percent_points_earned`). If the vendor changes these headers, update that mapping.

The `studentAssessmentIdentifier` is an MD5 hash of student ID, assessment identifier, and administration date. Re-loading the same file updates existing records instead of creating duplicates.

The input file must have a `.csv` extension, or `type: csv` must be set on the `input` source in `earthmover.yaml`.

### Included sample files

The bundle includes anonymized sample data covering:

- grade 5
- grade 8
- grade 11
- grade 11 retakes

Each file includes a student with `Insufficient to score` in every score column.

---

## 7. Things to validate for a new extract

Before assuming the existing mapping applies to a new WCAS extract, check:

- the exact scale-score and performance column names, including how retakes are labeled
- the values used for overall performance and reporting-area proficiency (every value must exist in `seeds/performanceLevelDescriptors.csv`)
- whether percents include a `%` sign
- the `Date Taken` and `Test Reason` formats
- any placeholder values other than `Insufficient to score`, `N/A`, or blank

---

## 8. Maintaining this bundle

Several values must be spelled identically in more than one file. When changing one, update the others:

| If you change... | Also update... |
| --- | --- |
| Namespace in `seeds/assessments.csv` | The `namespace` column in the other seeds |
| A performance level in `seeds/performanceLevelDescriptors.csv` | The hardcoded level lists in `templates/assessments.jsont` (overall) or `templates/objectiveAssessments.jsont` (reporting areas) |
| A reporting method in `seeds/assessmentReportingMethodDescriptors.csv` | Every template that names it after `#` |
| A reporting area (add, remove, rename) | `rename_columns` in `earthmover.yaml`, `seeds/objectiveAssessments.csv`, and the list in `templates/studentAssessments.jsont` |
| A tested grade | A row in `seeds/gradeLevelDescriptors.csv` |

`seeds/gradeLevelDescriptors.csv` and `seeds/academicSubjectDescriptors.csv` hold Ed-Fi default descriptors and are listed as descriptor mapping files in `_metadata.yaml`. Implementations that use different descriptors can remap them there.

---

## 9. CLI Parameters

- `OUTPUT_DIR`: Where output files will be written.
- `STATE_FILE`: Where to store the Earthmover runs.csv file.
- `INPUT_FILE`: The student assessment file to be mapped.
- `API_YEAR`: The API year of the ODS these records will be sent to.
- `STUDENT_ID_NAME`: Which input column should be used as the Ed-Fi `studentUniqueId`. Defaults to `edFi_studentUniqueID` (the column added by the student ID crosswalk feature); for the sample files use `Student ID`.

## 10. Output

The bundle produces Ed-Fi resources for:

- assessments
- objective assessments
- student assessments
- assessment reporting method descriptors
- assessment category descriptors
- performance level descriptors
- retest indicator descriptors

Only `studentAssessments` depends on the input file; the other resources are generated from the seeds and are the same on every run.

### Examples

Using an ID column from the assessment file:
```bash
earthmover run -c earthmover.yaml -f -p '{
"INPUT_FILE": "data/sample_anonymized_file_grade_5_wcas_summative_student_data.csv",
"STATE_FILE": "./runs.csv",
"OUTPUT_DIR": "output/",
"API_YEAR": "2026",
"STUDENT_ID_NAME": "Student ID"
}'
```

`-f` forces earthmover to regenerate output even if it thinks nothing has changed since the last run.

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with:
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```
