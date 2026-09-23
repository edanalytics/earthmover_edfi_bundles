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

## 3.3 Overall and area results won't always line up

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
[Cambium — Reporting System User Guide 2026–27](https://www.oregon.gov/ode/educator-resources/assessment/Documents/osas_reports_userguide.pdf)

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