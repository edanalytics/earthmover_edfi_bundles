## Test out the wrapper locally
earthmover run -p '{ 
"ASSESSMENT_BUNDLE": "your_bundle_here",
"INPUT_FILE": "./data/your_sample_file.csv",
"OUTPUT_DIR": "./output/", "API_YEAR": 2026}'

## Install deps
earthmover deps -p '{"ASSESSMENT_BUNDLE": "your_bundle_here"}'