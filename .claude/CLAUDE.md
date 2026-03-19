# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains pre-built assessment bundles for converting educational assessment data to the Ed-Fi standard format using [earthmover](https://github.com/edanalytics/earthmover). Output can be loaded to Ed-Fi ODSes using [lightbeam](https://github.com/edanalytics/lightbeam).

## Setup Requirements

### Slite MCP Server

This project is configured to access bundle creation documentation on Slite via the MCP (Model Context Protocol) server.

**Configuration:**

The Slite MCP server connection is configured in `.mcp.json` at the repository root:
```json
{
  "mcpServers": {
    "slite": {
      "type": "http",
      "url": "https://api.slite.com/mcp"
    }
  }
}
```

Authentication is handled by Claude Code's secure credential storage. No environment variables are required. If you need to reconnect, Claude Code will prompt for authentication when accessing Slite resources.

## Repository Structure

```
assessments/<BUNDLE_NAME>/
  earthmover.yaml          # Earthmover configuration
  lightbeam.yaml           # Lightbeam configuration
  _metadata.yaml           # Bundle metadata (generates registry.json)
  bundle_metadata.json     # CLI parameter and field requirements
  README.md                # Bundle-specific documentation
  data/                    # Sample anonymized files
  seeds/                   # Ed-Fi descriptor CSV files
  templates/               # Jinja2 .jsont files for JSON generation
  output/                  # Generated JSONL (gitignored)
```

## Critical Requirements

### Registry Synchronization

**ALWAYS regenerate registry.json after modifying any `_metadata.yaml` file.** PRs will fail CI if registry.json is out of sync.

Run: `python create-registry.py assessments --output registry.json`

Or use the `/sync-registry` skill.

### Testing Requirements

Bundles must be tested at multiple levels before opening a PR:

1. **Local Validation:** `earthmover run -c earthmover.yaml -p '{parameters}'` (use `/verify` skill)
2. **Ed-Fi ODS Integration:** `test-bundle` from [edfi_testing_stack](https://github.com/edanalytics/edfi_testing_stack)
3. **Runway Integration:** End-to-end testing with local Runway instance (optional but recommended)
4. **Warehouse Validation:** Verify downstream dbt transformations (if applicable)

See `.claude/rules/testing-guide.md` for complete testing workflow and `.claude/rules/quality-checklist.md` for review checklist.

### Sample File Handling (PII Safety)

**⚠️ CRITICAL: Original sample files provided for bundle development often contain PII.**

**NEVER:**
- ❌ Copy, move, or modify original sample files
- ❌ Commit sample files containing PII to git
- ❌ Upload PII to cloud storage or share via unsecured channels

**ALWAYS:**
- ✅ Keep original samples in their secure location (read-only)
- ✅ Examine multiple samples to understand format changes year-over-year
- ✅ Generate anonymized versions for the repository `data/` directory
- ✅ Verify anonymized files contain NO PII before committing
- ✅ Use synthetic IDs (9999XXXXX range), remove names, replace dates

Sample files in repository `data/` directories must be fully anonymized with NO real student data.

See `.claude/rules/sample-data-handling.md` for complete workflow and anonymization procedures.

## Assessment Governance

Follow these rules when creating or modifying assessment bundles:

- **Assessment Identifier Structure**: `{Title} {Subject}` (e.g., "MAP Growth Reading", "STAR-SR")
  - Highest level at which scores exist (typically subject-level)
  - Do NOT include vendor name in identifier (captured by namespace)
  - Include assessment_family for cross-subject grouping
- **Namespace**: Use vendor's domain (e.g., `uri://www.nwea.org/map/`)
- **Hierarchy**: Capture true assessment structure using Assessment/ObjectiveAssessment relationships

See `.claude/rules/governance.md` for detailed standards and examples.

## Descriptor Namespaces

Critical namespace rules:

- **Assessment-specific descriptors** (assessmentReportingMethods, performanceLevel): Use vendor namespace, keep original codeValues
- **Non-assessment-specific descriptors** (gradeLevels, academicSubjects): Use default Ed-Fi namespace (`uri://ed-fi.org`)
- **resultDatatypeTypeDescriptor**: Use `${DESCRIPTOR_NAMESPACE}` parameter (default: `uri://ed-fi.org`)
- **Score preservation**: Do NOT normalize scores at integration—preserve vendor methodologies via custom descriptors

See `.claude/rules/descriptors.md` for detailed rules and examples.

## Template Best Practices

When working with .jsont templates:

- **Null Handling**: Build lists of non-null values at top of template, then loop (Ed-Fi rejects empty strings)
- **Grain Matching**: Output must match Ed-Fi entity grain (StudentAssessment unique on: AssessmentIdentifier, Namespace, StudentAssessmentIdentifier, StudentUniqueId)
- **Required Fields**: At least 1 performance level OR score result required per student assessment

See `.claude/rules/templates.md` for patterns and examples.

## Workflow

- Branch from `main` and open PRs against `main`
- **Handle sample files safely:** Examine originals (read-only), generate anonymized versions (see PII Safety above)
- Follow existing bundle structure when creating new bundles
- Use assessments/_template_bundle/ as starting point for new bundles
- Bundle creation workflow documentation exists on Slite (connect via MCP)

## Key Commands

- **Run earthmover**: `earthmover run -c earthmover.yaml -p '{parameters}'`
- **Visualize DAG**: `earthmover graph -c earthmover.yaml`
- **Generate registry**: `python create-registry.py assessments --output registry.json`
- **Validate and send with lightbeam**: `lightbeam validate+send -c ./lightbeam.yaml -p '{parameters}'`
- **Lint Python code**: `ruff check .` (or `ruff check --fix .` to auto-fix)
- **Format Python code**: `ruff format .`
- **Lint YAML files**: `yamllint .`

## Important Gotchas

- **Student ID crosswalking**: Optional feature for matching assessment IDs to Ed-Fi roster IDs; see `.claude/rules/student-ids.md` and packages/student_ids/README.md
- **Parameter defaults**: Each bundle has parameter defaults in bundle_metadata.json (e.g., `STUDENT_ID_NAME: 'edFi_studentUniqueID'`)
- **Earthmover version**: Bundles require earthmover v2 YAML format
- **Descriptor namespace**: All Ed-Fi descriptors use namespace URIs (default: `uri://ed-fi.org`)
- **Relative paths**: All paths in configs are relative (no BUNDLE_DIR environment variable since v0.4.0)
- **File naming**: Use `.yaml` (not `.yml`), snake_case for column names

## Detailed Documentation

The `.claude/rules/` directory contains in-depth implementation guidance:
- `sample-data-handling.md` - **PII safety and sample file workflow** (READ FIRST)
- `governance.md` - Assessment identifier & hierarchy standards
- `descriptors.md` - Descriptor namespace rules and score preservation
- `templates.md` - Template engineering patterns and null handling
- `testing-guide.md` - Complete testing workflow (local, ODS, Runway, warehouse)
- `quality-checklist.md` - Complete bundle review checklist
- `student-ids.md` - Student ID crosswalking implementation

## Common Bundle Parameters

Most bundles accept these parameters:
- `INPUT_FILE`: Assessment data file (required)
- `OUTPUT_DIR`: Output directory (default: ./output/)
- `STATE_FILE`: Earthmover state file (default: ./earthmover_state.csv)
- `STUDENT_ID_NAME`: Which column to use as studentUniqueId (default: edFi_studentUniqueID)
- `API_YEAR`: School year (required for some bundles)

Check each bundle's `bundle_metadata.json` for specific parameter requirements.
