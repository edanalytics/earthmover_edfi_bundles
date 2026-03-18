# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains pre-built data mapping bundles for converting various assessment data formats to Ed-Fi format using [earthmover](https://github.com/edanalytics/earthmover). Each bundle includes:
- CSV seed data (descriptors and reference data)
- JSON template files (`.jsont` files using Jinja2 syntax)
- YAML configuration files for transformation and API transmission

The converted Ed-Fi JSON can be loaded to Ed-Fi ODSes using [lightbeam](https://github.com/edanalytics/lightbeam).

## Repository Structure

```
assessments/              # Individual assessment bundles (ACCESS, ACT, MAP, STAR, etc.)
  <ASSESSMENT_NAME>/
    earthmover.yaml       # Earthmover transformation configuration
    lightbeam.yaml        # Lightbeam API transmission configuration
    bundle_metadata.json  # Bundle metadata for Runway compatibility
    _metadata.yaml        # Registry metadata (for registry.json generation)
    data/                 # Sample anonymized input files
    seeds/                # Ed-Fi descriptor reference data (CSV)
    templates/            # Ed-Fi JSON templates (.jsont Jinja2 files)
    output/               # Generated JSONL output (gitignored)
    graph.png/.svg        # Visualization of data flow
    README.md             # Bundle-specific documentation
  _template_bundle/       # Template for creating new bundles

packages/                 # Reusable earthmover packages
  student_ids/            # Student ID crosswalking logic
  student_id_wrapper/     # Wrapper for student ID alignment

registry.json             # Generated registry of all bundles
create-registry.py        # Script to regenerate registry.json
```

## Running Assessment Bundles

### Basic earthmover execution (without student ID xwalking):
```bash
earthmover run -c ./earthmover.yaml -p '{
  "STATE_FILE": "./runs.csv",
  "INPUT_FILE": "data/sample_anonymized_file.csv",
  "OUTPUT_DIR": "output/",
  "STUDENT_ID_NAME": "<id_column_name>",
  "API_YEAR": "2023"
}'
```

### Transmitting to Ed-Fi ODS with lightbeam:
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
  "DATA_DIR": "./output/",
  "EDFI_API_BASE_URL": "https://api.example.com",
  "EDFI_API_CLIENT_ID": "client_id",
  "EDFI_API_CLIENT_SECRET": "client_secret",
  "API_YEAR": "2023"
}'
```

## Bundle Architecture

### Earthmover Configuration (earthmover.yaml)
- **version**: Always `2`
- **config**: Global settings (log_level, output_dir, memory_limit, parameter_defaults, macros)
- **sources**: Input files (assessment data + seed CSV files)
- **transformations**: Data manipulation pipeline (filter, join, group, modify columns)
- **destinations**: Output JSONL files with associated templates

### Key Transformation Patterns
1. **Student ID column standardization**: Always duplicate the chosen ID column to `student_unique_id`
2. **Snake case normalization**: Use `snake_case_columns` operation at end of transformations
3. **Date formatting**: Convert dates to ISO format (`YYYY-MM-DD`)
4. **Descriptor joins**: Join seed files for gradeLevelDescriptors, academicSubjectDescriptors, etc.

### Template Files (.jsont)
- Use Jinja2 syntax with double curly braces: `{{column_name}}`
- Reference Ed-Fi data model structure
- Common pattern for score results:
  ```jinja
  {%- set possible_scores = [
      [column1, "Score Name", "DataType"]
  ] -%}
  {%- set scores = [] -%}
  {%- for score in possible_scores -%}
    {%- if score[0] is not none and score[0] | length -%}
      {%- set _ = scores.append(score) -%}
    {%- endif -%}
  {%- endfor -%}
  ```

### Seed Files
- **assessments.csv**: Assessment metadata (identifier, title, subjects, grades)
- **objectiveAssessments.csv**: Sub-assessment definitions (subscores, standards)
- **performanceLevelDescriptors.csv**: Performance level definitions
- **assessmentReportingMethodDescriptors.csv**: Score reporting methods
- **gradeLevelDescriptors.csv**: Grade level mappings
- **academicSubjectDescriptors.csv**: Subject area mappings

## Student ID Xwalking Feature

The `packages/student_ids` and `packages/student_id_wrapper` packages automatically match student IDs from assessment files to Ed-Fi roster data.

### Key Parameters:
- `POSSIBLE_STUDENT_ID_COLUMNS`: Comma-separated list of columns that may contain student IDs
- `EDFI_STUDENT_ID_TYPES`: Comma-separated list of Ed-Fi ID types (Local, District, State)
- `EDFI_ROSTER_SOURCE_TYPE`: "file" or "database"
- `EDFI_ROSTER_FILE`: Path to studentEducationOrganizationAssociations.jsonl
- `EARTHMOVER_NODE_TO_XWALK`: The source node to crosswalk (e.g., `$sources.input`)
- `REQUIRED_ID_MATCH_RATE`: Minimum match rate threshold (e.g., 0.5)

The package produces:
- `best_id_match_rates.csv`: Match rate results (can be reused)
- `input_no_student_id_match.csv`: Unmatched student records

## Registry Management

The `registry.json` file is generated from `_metadata.yaml` files in each assessment bundle:

```bash
python create-registry.py assessments --output registry.json
```

**Important**: Always regenerate registry.json after modifying `_metadata.yaml` files. The GitHub workflow `.github/workflows/check-registry.yaml` validates this on PRs.

## Bundle Development Best Practices

When creating or modifying bundles:

1. **Start from _template_bundle**: Copy `assessments/_template_bundle` as starting point
2. **Student ID xwalking**: Include student ID xwalking logic (default parameter `STUDENT_ID_NAME: 'edFi_studentUniqueID'`)
3. **Descriptor seed files**: Never hardcode descriptor values in templates; always use seed files
4. **Sample data**: Include anonymized sample file in `data/` directory (NEVER commit PII)
5. **Naming conventions**:
   - No vendor names in assessment identifiers or folder names
   - Use `.yaml` (not `.yml`) for config files
   - Use relative paths
6. **Documentation**: Include comprehensive README with CLI parameters and examples
7. **Visualization**: Generate graph with `earthmover graph -c earthmover.yaml`
8. **bundle_metadata.json**: Include compatibility info (edfi_data_model_version_range, assessment_year_validated_range, required_fields, optional_fields, student_id_names)

## Common Commands

Generate DAG visualization:
```bash
earthmover graph -c earthmover.yaml
```

Validate configuration:
```bash
earthmover run -c ./earthmover.yaml --help
```

Fetch Ed-Fi roster data for student ID matching:
```bash
lightbeam fetch -s studentEducationOrganizationAssociations \
  -k studentIdentificationCodes,educationOrganizationReference,studentReference \
  -c lightbeam.yaml
```

## Testing Changes

- Run earthmover with sample data before committing
- Verify output JSONL files contain expected data
- Validate against Ed-Fi ODS if available
- Check that registry.json regenerates correctly if modifying _metadata.yaml

## Ed-Fi Standards Compatibility

Bundles aim for compatibility with Ed-Fi Data Standards 3.x, 4.x, and 5.x. Check individual bundle `bundle_metadata.json` for specific version requirements.

Key Ed-Fi resources:
- [Ed-Fi Data Standard 4](https://edfi.atlassian.net/wiki/spaces/EFDS4X/overview)
- [Ed-Fi Data Standard 5](https://edfi.atlassian.net/wiki/spaces/EFDS5/overview)
- [Assessment Data Governance best practices](https://edanalytics.slite.page/p/FwwhB84DoYVjY1/Assessment-Data-Governance-in-Ed-Fi)

## Git Workflow

- Main branch: `main`
- Create feature branches for new bundles or changes
- PRs trigger registry validation workflow
- Use conventional commit messages
