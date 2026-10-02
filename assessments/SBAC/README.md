* **Title**: Smarter Balanced Assessment Consortium (SBAC) Summative Assessments
* **Description**: Maps Smarter Balanced summative assessment results in English Language Arts/Literacy and Mathematics into Ed-Fi. Smarter Balanced is a multi-state consortium, so this bundle is deliberately written to support the shared assessment structure without assuming the policies or reporting practices of any one member state.
* **Submitter name**: Angelica Lastra
* **Submitter organization**: Education Analytics

> **Status: under development.**

## Model

This bundle is for the **Smarter Balanced Summative Assessment only**.

Smarter Balanced has a broader assessment system that also includes interim assessments such as ICAs, IABs, and Focused IABs, as well as formative instructional resources. Those are related to the same overall Smarter Balanced framework, but they are **not handled by this bundle**.

The summative assessment is the end-of-year assessment in:

- **English Language Arts/Literacy (ELA)**
- **Mathematics**

### Grade levels and high-school testing

Smarter Balanced describes its summative assessment as covering **grades 3–8 and high school**.

The high-school piece needs a little more context: The traditional/common Smarter Balanced high-school summative is associated with **grade 11**, but member states determine how the high-school assessment is administered for their own accountability and graduation policies.

For example, California administers its required Smarter Balanced summative in grades 3–8 and 11, while Washington administers it in grades 3–8 and 10.

A state may also allow students to take or re-take the high-school assessment in a later grade. Washington, for example, allows qualifying students in grades 11 and 12 to take the grade 10 assessment for graduation-pathway purposes or to attempt a higher score.

Because of this, **“high school” should not be interpreted as “all students in grades 9–12 take SBAC.”** There is generally one primary high-school summative administration, with the exact grade and any later retake rules determined by the state.

For developers, it is useful to keep two grade concepts separate:

- **Assessment grade**: the grade-level assessment being taken, such as the Grade 10 ELA summative.
- **Grade when assessed**: the student's enrolled grade when they took that assessment.

These may differ for a retake. For example, a Grade 11 student could take a state's **Grade 10 ELA Summative** as a retake. In that case, the assessment is still the Grade 10 assessment, but the student's `whenAssessedGradeLevel` is Grade 11.

Grade 12 should therefore not automatically be interpreted as a distinct Grade 12 Smarter Balanced assessment. Depending on the state and source file, it may instead indicate that a Grade 12 student took or re-took the state's high-school assessment.

### Assessments

The bundle creates two assessment resources, split by academic subject:

| Assessment identifier | Subject |
| --- | --- |
| `SBAC_ELA` | English Language Arts |
| `SBAC_MATH` | Mathematics |

The assessment family is `SBAC`, and the assessment category is **State summative assessment**.

### Student assessment results

For each student assessment, the bundle maps the core result information available across Smarter Balanced summative implementations:

- **Scale Score**
- **Performance Level**
- **Assessment Grade Level**
- **Grade when assessed**
- **Administration date**
- **Retest indicator**

Smarter Balanced scale scores are reported on a continuous vertical scale that is roughly 2000–3000 and increases across grade levels.

Overall performance is reported using four achievement levels:

| Performance level | General meaning |
| --- | --- |
| Level 1 | Minimal understanding to apply the knowledge and skills needed for success. |
| Level 2 | Partial understanding to apply the knowledge and skills needed for success. |
| Level 3 | Adequate understanding to apply the knowledge and skills needed for success. |
| Level 4 | Thorough understanding to apply the knowledge and skills needed for success. |

States may use different public-facing labels for these levels, so the bundle uses the common numeric **Level 1–4** structure rather than relying on a state-specific label such as “Proficient,” “Standard Met,” or “Advanced.”

Source extracts may contain additional fields such as standard errors, error bands, claim results, or other reporting information. Those fields are not automatically assumed to exist across all member states and are not part of the core mapping unless explicitly supported by this bundle.

### Retakes

Retake behavior is state-specific.
The source file may identify a result as a retake and may include both the assessment's original grade and the student's grade when the retake occurred.

For example:

`Grade 10 ELA Summative - Grade 11 (RETAKE) Scale Score`

means:

- the student took the **Grade 10 ELA Summative**
- the student was in **Grade 11** when they took it
- the Ed-Fi `retestIndicator` should indicate a retest

This distinction is important for high-school results because states can have different rules for whether students in grades 11 or 12 may re-take a previously administered high-school assessment.

Do not infer retake eligibility from Smarter Balanced generally. The source state's assessment policy is the authority for when a later-grade administration is valid.

## Claims, targets, and reporting

Smarter Balanced organizes assessment content using **claims** and **targets**.

At a high level:

**Subject → Claim → Target → Item or Performance Task**

For ELA, the four claims are:

| Claim | Area |
| --- | --- |
| 1 | Reading |
| 2 | Writing |
| 3 | Speaking/Listening |
| 4 | Research/Inquiry |

For Mathematics, the four conceptual claims are:

| Claim | Area |
| --- | --- |
| 1 | Concepts and Procedures |
| 2 | Problem Solving |
| 3 | Communicating Reasoning |
| 4 | Modeling and Data Analysis |

Mathematics Claims 2 and 4 are commonly combined for reporting purposes.

Claims and targets are part of the **assessment design**, but their existence does not mean that every state provides a student-level result for each claim or target in its district extract. More on that below.

### Full vs. adjusted summative blueprints

Smarter Balanced has both **full** and **adjusted** summative blueprints.

The **full blueprint** contains more CAT items and provides enough evidence within each claim to support detailed individual claim reporting.

The **adjusted blueprint** is shorter. It reduces the number of CAT items while still covering the overall content domain. Because fewer items are available within an individual claim, **the adjusted blueprint does not support the same individual claim-level reporting as the full blueprint**.

Claims and targets still exist in the assessment design when the adjusted blueprint is used; they simply may not appear as individual student results.

Washington is a useful example. Washington uses the **adjusted summative blueprint**, so its district-level student results do not report the four individual ELA claims or the corresponding individual math claims even though those claims are still part of the underlying Smarter Balanced assessment design.

For developers, this means:

> **When this bundle was initially developed for WA, we did not have any claim evidence in our extracts, which means we could no integrate them in this bundle. If your implementation does provide claims, you will have to extend this bundle to host those appropiately.**

This bundle currently does **not** map student-level Smarter Balanced claim or target results.

## ELA Performance Task writing results

ELA Performance Tasks introduce another layer that is easy to confuse with claims.

**Narrative, Informational/Explanatory, and Opinion/Argumentative are not separate ELA claims or overall assessment scores.**

They describe the **purpose of an ELA full-write Performance Task**.

The terminology varies somewhat by grade:

| Writing purpose | Typical grades |
| --- | --- |
| Narrative | Grades 3–8 |
| Informational | Grades 3–5 |
| Explanatory | Grades 6–11 |
| Opinion | Grades 3–5 |
| Argumentative | Grades 6–11 |

A student's full-write response can then be scored on rubric traits such as:

- **Organization/Purpose**
- **Evidence/Elaboration**
- **Conventions**

For example, a source file might contain:

```text
Argumentative: Organization/Purpose
Argumentative: Evidence/Elaboration
Argumentative: Conventions
```

or, for a younger grade:

```text
Opinion: Organization/Purpose
Opinion: Evidence/Elaboration
Opinion: Conventions
```

These values describe the student's performance on the **full-write rubric**. They are not the same thing as the student's overall ELA scale score, achievement level, or Claim 2 Writing score.

### Objective Assessments in this bundle

When these ELA full-write rubric results are present in the source file, this bundle represents them as Ed-Fi `ObjectiveAssessment` / `StudentObjectiveAssessment` records.

For example:

```text
argumentative_organization_and_purpose
argumentative_evidence_and_elaboration
argumentative_conventions
```

The same pattern applies to the other supported ELA writing purposes.

These ObjectiveAssessments are therefore an **Ed-Fi representation of reported writing rubric results**. They should not be interpreted as the consortium's top-level ELA claims.

Mathematics does not currently produce equivalent writing-purpose ObjectiveAssessments in this bundle.

Because state extracts differ, the writing-purpose fields are treated as optional. Their absence from a district extract does not imply that the corresponding writing purpose or Performance Task is absent from Smarter Balanced's assessment design.

## State differences developers should expect

This bundle is deliberately state-agnostic, but Smarter Balanced implementations are not identical across states.

When onboarding a new state's extract, developers should validate at least the following before assuming an existing mapping applies:

- which high-school grade is used for the primary summative administration
- whether older students may take or re-take that high-school assessment
- whether the state uses the full or adjusted blueprint
- whether individual claim results are reported
- whether ELA writing-purpose rubric results are included in the district extract
- how retakes are identified in the source headers
- the exact column names used for scale scores and performance levels

The safest rule is:

> **Use the consortium documentation to understand what the assessment means, but use the state's source-file specification to determine what student-level results actually exist.**

## Expected source structure

The bundle is designed around Smarter Balanced student-result extracts with headers similar to the Cambium/CRS-style files used in the included examples.

The bundle identifies the assessment subject and assessment grade from the summative scale-score column name.

Examples include:

```text
Grade 3 ELA Summative Scale Score
Grade 10 MATH Summative Scale Score
Grade 10 ELA Summative - Grade 11 (RETAKE) Scale Score
```

The corresponding performance-level field follows the same naming pattern using `Performance`.

The bundle also expects information necessary to identify the student, administration date, school year, and retake status.

Because vendor/state exports can change, new implementations should be checked against the parsing assumptions in `earthmover.yaml` rather than assuming every Smarter Balanced CSV has identical headers.

### Included sample files

The bundle includes anonymized sample data covering several useful cases:

- elementary ELA
- middle-school ELA
- high-school ELA
- high-school Mathematics
- high-school ELA retakes
- high-school Mathematics retakes

These examples are intended to exercise different grade bands, performance levels, writing-purpose fields, and retake behavior.

## CLI Parameters

- `OUTPUT_DIR`: Where output files will be written.
- `STATE_FILE`: Where to store the Earthmover runs.csv file.
- `INPUT_FILE`: The student assessment file to be mapped.
- `API_YEAR`: The API year of the ODS these records will be sent to.
- `STUDENT_ID_NAME`: Which input column should be used as the Ed-Fi `studentUniqueId`.

## Output

The bundle produces Ed-Fi resources for:

- assessments
- objective assessments
- student assessments
- assessment reporting method descriptors
- assessment category descriptors
- performance level descriptors
- retest indicator descriptors

The exact `studentObjectiveAssessments` emitted for an ELA result depend on which optional writing-rubric fields are populated in the source record.

## Lightbeam

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with:

```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_BASE_URL": "yourURL",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"API_YEAR": "yourAPIYear" }'
```