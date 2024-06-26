This is an earthmover tutorial:
* **Title**: Earthmover Tutorial
* **Description**: This tutorial is an interactive set of steps to introduce you to Earthmover.
* **API version**: N/A

This bundle includes an example source file with fake data:
* <code>data/Results_File.csv</code>

then run the following earthmover command:
```bash
earthmover run -c earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"ACCESS_RESULTS_FILE": "data/Results_File.csv",
"OUTPUT_DIR": "output",
"STUDENT_ID_NAME": "StateStudentID",
"SCHOOL_YEAR" : "2024"}'
```

Runtime notes:
- This bundle will not run as is.
- You will need to follow the tutorial instructions to populate the templates and `earthmover.yaml` in order for it to run.
- This is to be used for training purposes only, and your changes should not be pushed to remote.

