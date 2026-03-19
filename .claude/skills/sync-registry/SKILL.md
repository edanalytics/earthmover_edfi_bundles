---
name: sync-registry
description: Regenerate registry.json from all _metadata.yaml files in assessment bundles
disable-model-invocation: true
---

Regenerate the registry.json file from all assessment bundle metadata files.

## When to use this skill

Use this skill after:
- Creating a new assessment bundle with a _metadata.yaml file
- Modifying any existing _metadata.yaml file
- Before opening a PR that includes bundle metadata changes

The CI workflow will fail if registry.json is out of sync with _metadata.yaml files.

## What this skill does

1. Run the registry generation script: `python create-registry.py assessments --output registry.json`
2. Report whether registry.json was updated
3. Show a git diff of registry.json changes

## Important notes

- Always run this after modifying _metadata.yaml files
- The registry.json file should be committed along with metadata changes
- This is required for PRs to pass CI validation
