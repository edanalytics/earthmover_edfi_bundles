Title: ACT Assessment Results
Description: American College Test Assessment Results
API version: 5.3
Submitter name: Ludmila Janda
Submitter organization: Education Analytics

To run this bundle, please add your own source file(s) and column(s):

### Required
- OUTPUT_DIR: Where output files will be written.
- BUNDLE_DIR: Parent folder of the bundle, where `earthmover.yaml` lives.
- INPUT_FILE: The path to the ACT .csv file you want to transform.

### Examples
Running an ACT file:
```bash
earthmover run -c ./earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"INPUT_FILE": "path/to/ACT.csv",
"OUTPUT_DIR": "./output"}'
```

Once you have inspected the output JSONL for issues, check the settings in `lightbeam.yaml` and transmit them to your Ed-Fi API with
```bash
lightbeam validate+send -c ./lightbeam.yaml -p '{
"DATA_DIR": "./output/",
"EDFI_API_CLIENT_ID": "yourID",
"EDFI_API_CLIENT_SECRET": "yourSecret",
"EDFI_API_YEAR": yourAPIYear }'
```

### Output Information
For each subject, the output will provide columns that are specific to that assessment: Score, State Rank, US Rank, and Superscore. For instance, for English this would be English Score, English State Rank, English US Rank, and English Superscore.
Here are the descriptions for each of those metrics:

Score: An integer that gives the score the student achieved for the given subject, on a scale of 0-36
State Rank: How the student ranked for the given subject within their state, on a scale on 0-100
US Rank: How the student ranked for the given subject within the US, on a scale on 0-100
Superscore:  The student's best subject scores from all of thier ACT test attempts

For the Reading assessment, there is one indicator, Reading Complex Test, which has the expected values of Below Proficiency; Proficient; Above proficiency; Unable to Calculate

For the Writing assessment, along with a Writing score, there are the following scores, which are scored on a scale of 2-12:
Writing Domain Ideas and Analysis Score
Writing Domain Development and Support Score
Writing Domain Organization Score
Writing Domain Language Use and Conventions Score

Along with the Composite Score, there are also the following metrics:
Sum of Scale Scores: the numeric sum of the four scale scores that are used for the Composite score (English, Math, Reading, Science)
Sum of Superscore Scale Scores: the numeric sum of the best of each of the four scale scores that are used for the Composite score (English, Math, Reading, Science) from all ACT Test Attempts