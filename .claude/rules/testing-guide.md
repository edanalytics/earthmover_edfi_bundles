# Bundle Testing Guide

This guide covers the complete testing workflow for earthmover assessment bundles, from local validation to integration testing with Runway and downstream warehouse validation.

## Testing Levels

Assessment bundles should be tested at multiple levels:

1. **Local Earthmover Validation** - Quick syntax and transformation checks
2. **Ed-Fi ODS Integration** - Validation against Ed-Fi API
3. **Runway Integration Testing** - End-to-end workflow testing
4. **Warehouse Data Validation** - Downstream dbt transformations

## Level 1: Local Earthmover Validation

### Quick Validation with earthmover run

**Purpose:** Verify YAML syntax, transformations, and template rendering.

**Command:**
```bash
cd assessments/<BUNDLE_NAME>
earthmover run -c earthmover.yaml -p '{
  "INPUT_FILE": "data/sample.csv",
  "API_YEAR": 2024
}'
```

**What to check:**
- [ ] Earthmover completes without errors
- [ ] Output files created in `output/` directory
- [ ] JSONL files are valid JSON (test with `jq`)
- [ ] Record counts match expectations
- [ ] No unexpected null values or missing fields

**Skill shortcut:** Use `/verify` skill for quick validation.

### Validate JSON Structure

Check that output is valid JSON:
```bash
jq . output/studentAssessments.jsonl > /dev/null
echo "Valid JSON: $?"  # Should output 0
```

Check for empty arrays (should return nothing):
```bash
cat output/studentAssessments.jsonl | jq 'select(.scoreResults == [] or .performanceLevels == [])'
```

Check for empty strings in scores:
```bash
cat output/studentAssessments.jsonl | jq '.scoreResults[]? | select(.result == "")'
```

### Verify Grain Uniqueness

Check for duplicate StudentAssessment records:
```bash
cat output/studentAssessments.jsonl | \
  jq -r '[.assessmentReference.assessmentIdentifier, .studentAssessmentIdentifier, .studentReference.studentUniqueId] | @csv' | \
  sort | uniq -d
```

Should return no results (empty means no duplicates).

### Visualize DAG

Check transformation logic flow:
```bash
earthmover graph -c earthmover.yaml
```

Opens a visualization of the transformation DAG in your browser.

## Level 2: Ed-Fi ODS Integration Testing

### Using test-bundle Command

**Purpose:** Validate bundle output loads successfully to Ed-Fi ODS.

**Prerequisites:**
- Access to [edfi_testing_stack](https://github.com/edanalytics/edfi_testing_stack)
- Running Ed-Fi ODS instance (local or remote)

**Command:**
```bash
# From edfi_testing_stack directory
test-bundle --bundle <BUNDLE_NAME> --input data/sample.csv --year 2024
```

**What test-bundle does:**
1. Runs earthmover with your sample data
2. Runs lightbeam validate to check Ed-Fi conformance
3. Runs lightbeam send to POST to ODS
4. Reports validation errors or success

**Common validation errors:**
- Empty strings in required fields
- Missing required descriptors
- Duplicate natural keys
- Invalid descriptor namespace/codeValue format
- Missing required associations

### Manual Ed-Fi API Validation

If test-bundle isn't available, manually test with lightbeam:

```bash
# Validate output
lightbeam validate -c lightbeam.yaml -p '{
  "INPUT_DIR": "output",
  "API_YEAR": 2024
}'

# Send to ODS
lightbeam send -c lightbeam.yaml -p '{
  "INPUT_DIR": "output",
  "API_YEAR": 2024,
  "EDFI_API_BASE_URL": "https://your-ods.example.com",
  "EDFI_API_KEY": "your-key",
  "EDFI_API_SECRET": "your-secret"
}'
```

### Check Ed-Fi ODS Logs

After sending, check ODS logs for warnings:
- Descriptor not found errors
- Validation rule violations
- Data type mismatches
- Foreign key constraint failures

### Query Ed-Fi ODS Directly

Verify data landed correctly:
```sql
-- Check StudentAssessments created
SELECT COUNT(*)
FROM edfi.StudentAssessment
WHERE AssessmentIdentifier LIKE '%YOUR_ASSESSMENT%';

-- Check score results
SELECT
  sa.StudentAssessmentIdentifier,
  sar.Result,
  arm.CodeValue as ReportingMethod
FROM edfi.StudentAssessment sa
JOIN edfi.StudentAssessmentScoreResult sar
  ON sa.StudentAssessmentIdentifier = sar.StudentAssessmentIdentifier
JOIN edfi.Descriptor arm
  ON sar.AssessmentReportingMethodDescriptorId = arm.DescriptorId
WHERE sa.AssessmentIdentifier LIKE '%YOUR_ASSESSMENT%';
```

## Level 3: Runway Integration Testing

**Purpose:** Test end-to-end workflow including file upload, job orchestration, and error handling.

### Prerequisites

#### 1. Local Environment Setup

**Required components:**
- Local Ed-Fi ODS + Airflow (via Stadium Sandbox)
- Local Runway application (frontend + API)
- Local S3 (MinIO)
- PostgreSQL database

**Setup documentation:** See [stadium_airflow_sandbox README](https://github.com/edanalytics/stadium_airflow_sandbox/blob/init-branch/README.md)

**Key configuration:**

**Add custom namespaces** (before running `sandboxer up`):
Edit `src/sandboxer/resources/edfi/docker/web-sandbox-admin/appsettings-modified.template.json`:
```json
{
  "User": {
    "NamespacePrefixes": [
      "uri://ed-fi.org",
      "uri://www.nwea.org/map/",
      "uri://your-vendor.com/assessment/"
    ]
  }
}
```

**Runway API configuration** (`runway/app/api/.env`):
```bash
OAUTH2_ISSUER=http://localhost:8080/realms/example
OAUTH2_AUDIENCE=runway-local

FE_URL=http://localhost:4200
MY_URL=http://localhost:3333
SESSION_SECRET=dummy-session-secret

POSTGRES_USER=app
POSTGRES_PASSWORD=dev
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=runway_local
POSTGRES_SSL=false

COMPOSE_PROJECT_NAME=runway_app
JWT_ENCRYPTION_KEY=super-secret-jwt-key
ODS_CREDS_ENCRYPTION_KEY=super-secret-keysuper-secret-key
S3_FILE_UPLOAD_BUCKET=runway-local-dev-data-integration

LOCAL_S3_ENDPOINT_URL=http://localhost:9090
LOCAL_EXECUTOR=python
LOCAL_BUNDLE_CACHE_DISABLED=true
BUNDLE_BRANCH=<YOUR_BUNDLE_BRANCH>
LOCAL_EVENT_EMITTER=log
AWS_REGION=us-east-2
```

#### 2. Start Runway Services

**Terminal 1 - API server:**
```bash
cd runway/app
npx nx run api:serve 2>&1 | tee /tmp/runway-api.log
```

**Terminal 2 - Frontend:**
```bash
cd runway/app
npx nx run fe:serve
```

**Terminal 3 - API log monitoring:**
```bash
tail -f /tmp/runway-api.log | grep -E "(runway|earthmover|lightbeam|ERROR)"
```

#### 3. Configure Runway Frontend

1. Open http://localhost:4200
2. Login: `dev` / `dev`
3. Add local ODS destination:
   - **Year:** 2025/26
   - **URL:** http://localhost:8001
   - **Key:** populatedKey
   - **Secret:** populatedSecret

#### 4. Register Bundle in Database

Connect to Runway postgres and register your bundle:

```sql
-- Add bundle
INSERT INTO earthmover_bundle (name, created_at, updated_at)
VALUES ('assessments/YOUR_BUNDLE', NOW(), NOW());

-- Associate with partner
INSERT INTO partner_earthmover_bundle (partner_code, earthmover_bundle_name)
VALUES ('ea', 'assessments/YOUR_BUNDLE');
```

Or use the Runway API/frontend to register the bundle if that workflow is available.

### Running Test Jobs

#### Using Runway Python Client

**Install client:**
```bash
git clone git@github.com:edanalytics/runway_python_client.git -b generalize-token-url
pip install -e runway_python_client
```

**Example test script:**
```python
from runway_client import RunwayClient

# Initialize client
client = RunwayClient(
    runway_base_url="http://localhost:3333/api/v1",
    auth_base_url="http://localhost:8080/realms/example/protocol/openid-connect/token",
    client_id="runway-api",
    client_secret="api-secret-123",
    partner_code="ea",
)

# Request job
job = client.request_runway_job(
    tenant_code="runway-local-example-tenant",
    bundle_name="assessments/YOUR_BUNDLE",
    school_year="2026",
    input_files={"INPUT_FILE": "path/to/test_data.csv"},
    bundle_params={
        "API_YEAR": 2026,
        "STUDENT_ID_NAME": "edFi_studentUniqueID"
    },
)

# Upload files to S3
client.upload_to_s3(job, {
    "INPUT_FILE": "path/to/test_data.csv"
})

# Start job
client.start_job(job)
print(f"Job started: {job['id']}")
print(f"Monitor at: http://localhost:4200/jobs/{job['id']}")
```

### Monitoring Job Execution

**Watch API logs:**
```bash
tail -f /tmp/runway-api.log | grep -E "(runway|earthmover|lightbeam|ERROR)"
```

**Key log messages:**
- `Downloading bundle from GitHub...` - Bundle fetching
- `Running earthmover...` - Transformation starting
- `looks ok` - Earthmover validation passed (but still running)
- `action: done` - Earthmover completed
- `Running lightbeam...` - Loading to Ed-Fi ODS
- `Successfully sent X records` - Lightbeam success
- `ERROR` - Something failed

**Note:** Earthmover may take several minutes after `looks ok` appears.

### Inspecting Job Output

**Check generated JSONL:**
```bash
cd runway/executor/local-run/output
ls -lh

# Validate JSON
jq . studentAssessments.jsonl | head -20

# Count records
wc -l studentAssessments.jsonl
```

**Review with user:**
- Do score values match source data?
- Are performance levels correct?
- Are objective assessment scores nested properly?
- Do descriptor namespaces look right?
- Are grade levels correct?

### Common Runway Testing Issues

**❌ Bundle not found**
- Check bundle registered in `earthmover_bundle` table
- Check `BUNDLE_BRANCH` in `.env` points to your branch
- Clear bundle cache: `LOCAL_BUNDLE_CACHE_DISABLED=true`

**❌ File upload fails**
- Check MinIO (local S3) is running: http://localhost:9090
- Check S3 bucket exists: `runway-local-dev-data-integration`

**❌ Earthmover fails**
- Check earthmover.yaml syntax
- Check parameter defaults in bundle_metadata.json
- Check file path references in sources

**❌ Lightbeam fails**
- Check descriptor seed files exist
- Check namespace format in templates
- Check ODS credentials in Runway frontend
- Check Ed-Fi ODS is running: http://localhost:8001

**❌ Job stuck in "running" state**
- Check API logs for errors
- Check earthmover/lightbeam process isn't hanging
- Restart API server if needed

## Level 4: Warehouse Data Validation

**Purpose:** Verify data flows correctly through dbt transformations into analytics tables.

### Prerequisites

- Local Airflow instance running (from Stadium Sandbox)
- Snowflake account access (`edanalytics-test`)
- dbt project configured (typically `edu_wh`)

### Trigger Data Pipeline

#### 1. Load Ed-Fi Resources to Snowflake

**Via Airflow UI** (http://localhost:8080):
1. Navigate to DAGs
2. Trigger `edfi_el_<tenant>_<year>_resources`
3. Wait for completion (~5-10 minutes)

**Or via CLI:**
```bash
# Access airflow scheduler container
docker exec -it <scheduler-container-id> bash

# Trigger DAG
airflow dags trigger edfi_el_grand_bend_2024_resources
```

#### 2. Run dbt Transformations

**Via Airflow UI:**
1. Trigger `run_dbt_dev`
2. Wait for completion (~10-15 minutes)

**Or via CLI:**
```bash
# From dbt project directory
dbt run --models student_assessments
dbt test --models student_assessments
```

### Query Warehouse Tables

**Check raw Ed-Fi data landed:**
```sql
-- Snowflake: edanalytics-test account
USE DATABASE <tenant>_edfi_<year>;
USE SCHEMA staging;

-- Count student assessments
SELECT COUNT(*)
FROM student_assessments
WHERE assessment_identifier LIKE '%YOUR_ASSESSMENT%';

-- Check score results
SELECT
    student_assessment_identifier,
    assessment_identifier,
    result,
    assessment_reporting_method_descriptor
FROM student_assessment_score_results
WHERE assessment_identifier LIKE '%YOUR_ASSESSMENT%';
```

**Check transformed analytics tables:**
```sql
USE DATABASE <tenant>_warehouse;
USE SCHEMA core;

-- Check fact table
SELECT
    k_student,
    k_assessment,
    k_school,
    school_year,
    score_result,
    performance_level
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%';

-- Check score formatting
SELECT DISTINCT
    score_type,
    score_result,
    performance_level
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
ORDER BY score_type;
```

### Adding dbt Seeds for Score Formatting

**Purpose:** Format score results and performance levels for reporting.

**Example seed file** (`seeds/assessment_score_formatting.csv`):
```csv
assessment_namespace,assessment_reporting_method,score_display_name,score_order
uri://www.nwea.org/map/,RIT Scale Score,RIT Scale Score,1
uri://www.nwea.org/map/,Percentile,Percentile,2
uri://act.org/act/,Composite Score,Composite,1
uri://act.org/act/,Scale Score,Scale Score,2
```

**Example seed file** (`seeds/assessment_performance_level_formatting.csv`):
```csv
assessment_namespace,performance_level_descriptor,level_display_name,level_order
uri://www.nwea.org/map/,uri://www.nwea.org/map/PerformanceLevelDescriptor#High Average,High Average,4
uri://www.nwea.org/map/,uri://www.nwea.org/map/PerformanceLevelDescriptor#Low Average,Low Average,2
```

**Load seeds:**
```bash
dbt seed
dbt run --models +fct_student_assessments
```

### Validation Queries

**Check score distribution:**
```sql
SELECT
    score_type,
    COUNT(*) as record_count,
    MIN(score_result::float) as min_score,
    MAX(score_result::float) as max_score,
    AVG(score_result::float) as avg_score
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
GROUP BY score_type;
```

**Check performance level distribution:**
```sql
SELECT
    performance_level,
    COUNT(*) as student_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
AND performance_level IS NOT NULL
GROUP BY performance_level
ORDER BY student_count DESC;
```

**Check for data quality issues:**
```sql
-- Missing scores
SELECT COUNT(*)
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
AND score_result IS NULL
AND performance_level IS NULL;

-- Invalid grade levels
SELECT DISTINCT grade_level
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
ORDER BY grade_level;

-- Check for duplicates
SELECT
    k_student,
    k_assessment,
    student_assessment_identifier,
    COUNT(*) as record_count
FROM fct_student_assessments
WHERE assessment_title LIKE '%YOUR_ASSESSMENT%'
GROUP BY 1,2,3
HAVING COUNT(*) > 1;
```

## Complete Testing Checklist

Before opening a PR, complete all testing levels:

### ✓ Local Validation
- [ ] `earthmover run` completes without errors
- [ ] Output JSONL is valid JSON
- [ ] No empty arrays or empty strings
- [ ] No duplicate StudentAssessment records
- [ ] Record counts match expectations

### ✓ Ed-Fi ODS Integration
- [ ] `test-bundle` passes (or manual lightbeam send succeeds)
- [ ] No Ed-Fi validation errors
- [ ] Data appears in ODS tables
- [ ] Descriptors are recognized
- [ ] Score results and performance levels correct

### ✓ Runway Integration (if available)
- [ ] Bundle registered in Runway database
- [ ] Test job completes successfully
- [ ] No errors in API logs
- [ ] Output JSONL matches expectations
- [ ] File upload/download works

### ✓ Warehouse Validation (if applicable)
- [ ] Data loads to Snowflake staging tables
- [ ] dbt transformations succeed
- [ ] Data appears in analytics tables
- [ ] Score distributions look reasonable
- [ ] Performance level distributions make sense
- [ ] No unexpected nulls or duplicates

## Troubleshooting

### Earthmover Issues

**"Column not found" error:**
- Check source data columns match what's referenced in transformations
- Check for typos in column names
- Check case sensitivity

**"Template rendering failed" error:**
- Check Jinja syntax in .jsont templates
- Check for missing variables
- Check conditional logic

**Empty output files:**
- Check source data isn't being filtered out
- Check transformations aren't removing all rows
- Check file paths in earthmover.yaml

### Lightbeam Issues

**"Descriptor not found" error:**
- Check seed files exist and are loaded
- Check descriptor namespace format
- Check codeValue matches exactly

**"Duplicate key" error:**
- Check studentAssessmentIdentifier uniqueness
- Check grain of transformations
- Check for multiple assessments with same identifier

**"Required field missing" error:**
- Check template has all required Ed-Fi fields
- Check conditional logic isn't skipping required fields

### Warehouse Issues

**Data not appearing in staging:**
- Check Airflow DAG succeeded
- Check Ed-Fi ODS has data
- Check date ranges in extraction logic

**Data missing in analytics tables:**
- Check dbt models ran successfully
- Check join conditions in dbt models
- Check filters in dbt models

**Score formatting looks wrong:**
- Check seed files loaded
- Check seed values match descriptor namespaces exactly

## References

- **Stadium Sandbox:** https://github.com/edanalytics/stadium_airflow_sandbox
- **edfi_testing_stack:** https://github.com/edanalytics/edfi_testing_stack
- **Runway:** https://github.com/edanalytics/runway
- **Quality Checklist:** `.claude/rules/quality-checklist.md`
- **Governance Rules:** `.claude/rules/governance.md`
