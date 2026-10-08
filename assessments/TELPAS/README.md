* **Title**: Texas English Language Proficiency Assessment System (TELPAS)
* **Description**: Maps the TEA (Cambium) TELPAS and TELPAS Alternate *Reporting Student Data Files* (fixed-width `.txt`) to Ed-Fi.
    * TELPAS, grades K-12 (compatibility from 2021-22 to 2025-26)
    * TELPAS Alternate, grades 2-12 (compatibility from 2021-22 to 2025-26)
* **Submitter name**: Tom Reitz
* **Submitter organization**: Education Analytics

File layouts are published by TEA on the [student assessment results](https://tea.texas.gov/student-assessment/student-assessment-results) page (e.g. [2026 TELPAS](https://tea.texas.gov/data-reports/student-assessment-results/2026-telpas-data-file-layout.pdf), [2026 TELPAS Alternate](https://tea.texas.gov/data-reports/student-assessment-results/2026-telpas-alt-data-file-layout.pdf)).


## CLI Parameters

### Required
- `INPUT_FILE`: path to the TEA TELPAS or TELPAS Alternate fixed-width `.txt` file
- `API_YEAR`: the Ed-Fi API year (spring of the school year), e.g. `2026` for 2025-2026. Also selects the year's file layout.
- `FORMAT`: `Standard` (TELPAS) or `Alternate` (TELPAS Alternate)

### Optional
- `STUDENT_ID_NAME`: the input column to use as `studentUniqueId`. Defaults to `edFi_studentUniqueID` (the column added by the student ID xwalk package). Without the xwalk, use one of: `tx_unique_student_id` (TSDS ID), `local_student_id`.
- `OUTPUT_DIR` (default `./output`), `STATE_FILE` (default `./runs.csv`), `DESCRIPTOR_NAMESPACE` (default `uri://ed-fi.org`, used for `ResultDatatypeTypeDescriptor`s)

### Examples
TELPAS:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file_telpas.txt",
"API_YEAR": "2026",
"FORMAT": "Standard",
"STUDENT_ID_NAME": "tx_unique_student_id"
}'
```
TELPAS Alternate:
```bash
earthmover run -c ./earthmover.yaml -p '{
"INPUT_FILE": "./data/sample_anonymized_file_telpas_alt.txt",
"API_YEAR": "2026",
"FORMAT": "Alternate",
"STUDENT_ID_NAME": "tx_unique_student_id"
}'
```
Run from this folder: the proficiency-rating `map_file`s are resolved relative to the working directory.

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```


## Ed-Fi structure
```
telpas  (TELPAS)                               telpas_alt  (TELPAS Alternate)
│ Composite Rating (PL), Composite Score,      │ Composite Rating (PL), Composite Score,
│ Yearly Progress Indicator, Administration    │ Yearly Progress Indicator, Administration
│ Code, Enrolled Grade, Rater Info-A/B,        │ Code, Score Code, Non-Participant
│ accommodations                               │
├── Listening ── Reporting Category 1, 2, 3    ├── Listening ── Reporting Category 1, 2
├── Speaking  ── Reporting Category 1, 2       ├── Speaking  ── Reporting Category 1, 2
├── Reading   ── Reporting Category 1, 2, 3    ├── Reading   ── Reporting Category 1, 2, 3
└── Writing   ── Reporting Category 1, 2       └── Writing   ── Reporting Category 1, 2
```
* Namespace `uri://tea.texas.gov/student-assessment`; both assessments share `assessmentFamily` `TELPAS`.
* Domain objective assessments (`Listening`, ...) carry the Proficiency Rating (PL), and, where present, Score Code, Tested Grade, Raw Score, Scale Score, Holistic Rating Test Administration (Paper Test Administration for Reading), and Non-Participant.
* Reporting category objective assessments (`Listening Reporting Category 1`, ...) are children of their domain and carry a Raw Score. TEA's layouts don't name the categories, so the identification codes use TEA's generic labels.
* `studentAssessmentIdentifier` is TEA's Opportunity Key (falls back to Test Result ID).
* `whenAssessedGradeLevelDescriptor` is the first non-blank domain Tested Grade (TELPAS, 2023+), else the file's grade. TELPAS also sends the enrolled grade as an `Enrolled Grade` score.
* Not mapped: demographics, item-level fields (points by item, responses), and the prior-year historical blocks.


## Layout differences by year
Each `fwf_to_csv_xwalks/{telpas,telpas_alt}_fwf_xwalk_{year}.csv` maps one year's layout to conformed column names, so templates are year-agnostic. Differences that affect output:

| Year | TELPAS |
|---|---|
| 2022 | No per-domain Tested Grade; Writing holistic only (no raw/scale/reporting category scores); no Writing Speech-to-Text; accommodations are Reading-only (mapped to the Reading and Writing descriptors) |
| 2022-2023 | Opportunity Key / Test Result ID / Non-Participant at positions 1106-1152 |
| 2023 | No Yearly Progress Indicator |
| 2022-2025 | One Non-Participant flag for Listening/Speaking and one for Reading/Writing; each is sent on both domains |
| 2026 | Non-Participant per domain |

(TELPAS Alternate score fields are unchanged across 2022-2026.)

To add a year: copy the latest colspec files, adjust positions per TEA's new layout (see [here](https://tea.texas.gov/data-reports/student-assessment-results/data-file-formats)), and add to the table above.


## Design decisions
Decision points worth reviewing:

1. **Separate bundle from STAAR**: TELPAS measures English language proficiency, not content mastery; modeled as its own assessments.
2. **Two assessment identifiers**: `telpas` and `telpas_alt` (like `ACCESS`/`Alternate-ACCESS`) because the tests differ in composition and rating scales; linked via `assessmentFamily` `TELPAS`.
3. **Assessment categories**: `State English proficiency test` (TELPAS), `State alternate assessment/ELL` (TELPAS Alternate). Academic subject `English` (matching ACCESS).
4. **Descriptor namespace matches STAAR**: `uri://tea.texas.gov/{AssessmentReportingMethod,PerformanceLevel,Accommodation}Descriptor`, so TEA descriptors live together downstream.
5. **Proficiency ratings are sent as TEA's labels, not codes** (e.g. `4` becomes `Advanced High`, Alternate `5` becomes `Basic Fluency`, `0` becomes `No Rating Available`). This departs from the "send codes as-is" guidance because:
    * `uri://tea.texas.gov/PerformanceLevelDescriptor#1`-`#4` are already used by STAAR Interim (Does Not Meet ... Masters), and TELPAS and TELPAS Alternate codes would also collide with each other.
    * STAAR Summative already sends text labels (`Did Not Meet` ... `Masters`) in the same namespace.
    * Labels come verbatim from TEA's layouts, have been stable since 2022, and remove the need for code-to-label crosswalks downstream.

    The crosswalks are `seeds/proficiency_rating_xwalk_{telpas,telpas_alt}.csv`.
6. **Administration date**: TEA's file has only an `MMYY` administration code (`0326` = Spring 2026), so `administrationDate` is the 1st of that month (`2026-03-01`). This avoids a yearly-maintained window seed (cf. STAAR Summative). The raw code is also sent as an `Administration Code` score.
7. **Item-level results not mapped** (like most other bundles).
8. **Fixed-width only**: TEA delivers TELPAS as `.txt`; no CSV variant is supported.

Judgment calls that need review/discussion:

9. **Subject:** English, matching ACCESS. Ed-Fi also has English Language Learners.
10. **Reporting categories** are coded generically (Listening Reporting Category 1, etc.) because TEA's layouts don't name them.
11. **Fixed-width .txt** input only; no CSV variant.
12. Raw and scale scores **keep the file's leading zeros (0645)** (as STAAR does).


## Sample data
`data/` contains anonymized and synthetic (fake) records only: `sample_anonymized_file_telpas.txt` (2026 TELPAS: K holistic plus synthetic grades 1-9 online/absent/not-tested records) and `sample_anonymized_file_telpas_alt.txt` (2026 TELPAS Alternate, synthetic).
