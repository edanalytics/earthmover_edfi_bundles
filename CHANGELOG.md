# Unreleased
## New features

## Under the hood

## Fixes

# earthmover_edfi_bundles v0.2.2
## New features
- South Carolina Alternate Assessment Bundle

## Fixes
- Capitalize student ID columns for TX-KEA bundle to work with the student ID wrapper
- Update 2024 entries in the administration window xwalk and removes a blank descriptor field in STAAR Summative bundle
- Fix academic subject array structure in MAP Fluency bundle

# earthmover_edfi_bundles v0.2.1
## New features
- MAP Reading Fluency Bundle

## Under the hood
- Add parameter defaults for output and temp dir for the student ID and student ID wrapper packages
- Expand the objective assessment codes xwalk for STAAR Interim to include 2022, 2024, and 2025
- Remove DIBELS 8 records with empty dates
- Add compatibility with the student ID package to the IB bundle

## Fixes
- Add quotes around values to fix an issue with writing out a non-matched students file when there are commas in the data

# earthmover_edfi_bundles v0.2.0
## New features
This release adds two packages that offer better functionality for handling student IDs:

1. `student_ids`: This package will merge all student IDs from an assessment file against all IDs from an Ed-Fi studentEducationOrganizationAssociation file/database source to determine the highest merge rate and remove student assessment records without a matching roster record. See the README file in the package folder for more detailed functionality information.

2. `student_id_wrapper`: This package uses [project composition](https://github.com/edanalytics/earthmover?tab=readme-ov-file#project-composition) to combine the student id package with any assessment bundle, which is passed as a parameter. See the README file in the package folder for more detailed functionality information.

Additionally, the SC Ready assessment bundle was added to this release.

## Under the hood
This release also contains a major refactor of all existing assessment bundles, which include:

1. Updating the assessment bundles to be compatible with the `student_id` package.

2. Improving the assessment bundles for better consistency and to follow the best practices:
    - Adding an anonymized sample file for better testing.
    - Removing the `BUNDLE_DIR` parameter and replaced with relative pathing.
    - Removing the vendor from folder names.
    - Removing any hardcoded descriptors from the templates and moving to seeds.
