---
name: verify
description: Validate an assessment bundle by running earthmover against sample data
---

Run earthmover against sample data to verify an assessment bundle generates valid Ed-Fi JSON output.

## When to use this skill

Use this skill:
- After creating or modifying a bundle
- Before opening a PR
- To test earthmover configuration changes
- To verify template (.jsont) changes produce correct output

## What this skill does

1. Identify which bundle to test (from current directory or user specification)
2. Check for sample data files in the bundle's `data/` directory
3. Run earthmover with appropriate parameters against the sample data
4. Report any errors or validation issues
5. Show summary of generated output files

## Usage

When the user runs `/verify`, determine:
- Which bundle to test (if in a bundle directory, use that bundle; otherwise ask)
- Which sample data file to use (check bundle's data/ directory)
- What parameters the bundle requires (check bundle_metadata.json)

Then run:
```bash
cd assessments/<BUNDLE_NAME>
earthmover run -c earthmover.yaml -p '{"INPUT_FILE": "data/<sample_file>", "OUTPUT_DIR": "./output/", "STATE_FILE": "./earthmover_state.csv"}'
```

Add any required parameters from bundle_metadata.json (e.g., API_YEAR, STUDENT_ID_NAME).

## Notes

- This skill only validates that earthmover runs successfully and generates output
- Full validation requires testing against an Ed-Fi ODS instance (not automated)
- Check the output/ directory for generated JSONL files
- Review earthmover logs for warnings or errors
