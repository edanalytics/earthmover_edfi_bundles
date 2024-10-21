# Earthmover Tutorial

# Overview

## What is this document?

This document is a step by step tutorial introducing you to Earthmover as a tool - its components and how to run it. The target audience is a data engineer who has never used Earthmover before and who is going to be developing an EM assessment bundle.

## What is NOT in this document?

This tutorial will not teach you how to build a bundle in full. For details on how to write an Earthmover bundles with assessments in mind, see [Writing earthmover bundles to integrate assessment data into Ed-Fi](https://slite.com/api/public/notes/LKGIWG-7-2-rqD/redirect) .

This tutorial will also not allow you to run lightbeam because there is no ODS that has corresponding sample data.

## Prerequisites

You should have working knowledge of the following:

-   [YAML](https://realpython.com/lessons/yaml-introduction/)
-   [Jinja](https://www.getdbt.com/dbt-learn/lessons/intro-to-jinja#1)
-   JSON
    -   jsont
    -   jsonl

# Step 0: Initial Setup

-   Clone the repo <https://github.com/edanalytics/earthmover_edfi_bundles>
-   `git checkout` a new branch for your tutorial work. There is no need to push this branch up to remote.
-   `cd` to the `tutorial/` directory

# Step 1: Introduction to the directory structure

## Files in an EM bundle

Each of these are files that you will need to populate for your EM/LB project. It's not a bad idea to copy and paste from existing bundles, both for inspiration and for consistency.

-   `earthmover.yaml` - This is a config file that defines a list of "instructions" that are run on the data files before they get transformed by the template files.
-   `lightbeam.yaml` - This is a lightbeam config file which is required to run lightbeam. Ignore for this tutorial, but it is worth noting that it exists in a bundle.
-   `README.md` - The readme should include information on how to run this bundle, including instructions for configuration specific to the bundle.

## Directories in an EM bundle

-   Inputs
    -   `data/` - This contains input data sources. Typically, these are your student assessment files. This directory may have a `.gitkeep` but it will typically be empty in remote. You don't want to push your student assessment files to remote. In the tutorial bundle, we've included a very simple fake assessment.
    -   `seeds/` - This contains input data sources. You will be creating and populating these, and they should be applicable to any implementation of this bundle. Typically, these are assessment metadata (e.g., name, scores) and descriptors (e.g., performanceLevelDescriptors)
-   Templates
    -   `templates/` - This contains the jsont (json template) files that define how your flat files (in `data/` and `seeds/`) will get transformed into jsonl (json lines).
-   Outputs
    -   `output/` - This contains your jsonl (json lines) output files. It will be be empty in the remote bundle, but contain a `.gitkeep`. These are your input sources that have been converted into json lines. Please note that you don't want to push student assessment output files to remote.

## Earthmover flow diagram

[See the EM README for a diagram of the earthmover flow](https://github.com/edanalytics/earthmover?tab=readme-ov-file#dag)

In this diagram:

-   Sources = the csv (or other format) files in `data/` and `seeds/` which need to be populated before you run earthmover
-   Transformations = (1) Any configuration defined in `earthmover.yaml` , then (2) json templates defined in `templates/`
-   Destinations = the `.jsonl` files in `output/` that are generated after you run earthmover

# Step 2: Investigate the tutorial files

## About `earthmover.yaml`

Open `earthmover.yaml` and take a look at it. This is currently a shell, and this tutorial will guide you through steps to fill it out.

**HINT: In VS Code, when viewing the `earthmover.yaml` file, set the Language Mode to "Jinja YAML".**

Notice that there are 4 main sections in this config file:

-   **config** - leave these as they are, they will be filled out later
-   **sources** - this is how you tell earthmover what and where your input files are (from `data/` and `seeds/`). Earthmover will read them in as dataframes with the names you define.
-   **transformations** - these will be instructions on the transformations that you want to perform on the source files before they get read into the json templates
-   **destinations** - these are the names of the output files that you want earthmover to create. Each destination file requires a source, and this source can either be a raw source (usually seed files), or a transformed source (usually data files).

**HINT: You can use variables in the earthmover.yaml file like: `${VARIABLE_NAME}`. These variable names will come from your runtime parameters, for example: `-p '{"RESULTS_FILE": "EA_Summative.csv"}'`**

## About `data/`

This is where your input data files will live. These are distinct from seed files, which contain metadata. `data/` files will typically be student assessment result files that come from the assessment vendor.

# Step 3: Walking through an example

## Create a seed file

Let's create a seed file to define what this assessment in Results_File is. This is metadata that will be sent to Ed-Fi, and it would live in the assessments endpoint (eventually making it to dim_assessment).

Create a file named `assessments.csv` and populate it with the following:

```csv
assessmentIdentifier,assessmentTitle,namespace,assessmentCategoryDescriptor,academicSubjectDescriptor
SUMMATIVE-Math,Year End Summative Assessment,uri://fake.ea.edu/assess/summative,uri://ed-fi.org/AssessmentCategoryDescriptor#State high school subject assessment,uri://ed-fi.org/AcademicSubjectDescriptor#Mathematics
```

In this seed file, we're specifying the metadata for one assessment - the `SUMMATIVE-Math` assessment.

## Define the source

Now that we have an input file, we need to tell earthmover that it's going to be one of our data sources. Go back to `earthmover.yaml` , and we'll add this seed file to the `sources` section. Copy and paste the section in the code block below.

```yaml
sources:
  assessments:
    file: ${BUNDLE_DIR}/seeds/assessments.csv
    header_rows: 1
```

From here on out, whenever we refer to `assessments` in the `earthmover.yaml` , earthmover knows that we're referring to the data in `assessments.csv` (which earthmover will read in as a dataframe).

**HINT: `${BUNDLE_DIR}` is another example of a parameter that will be passed in at runtime. `-p '{"BUNDLE_DIR": "."}'`**

## Define transformations

After defining your source, the next step will be to (optionally) define transformations. Typically, your seed files won't require transformations because you probably have control over their shape, and can therefore apply any transformations before they become seeds. The bulk of your transformations are going to be applied to your input files (assessment data).

We won't be applying any transformations to the assessments, but know that this is where transformations would happen.

## Create a template

We're going to create a template for assessments. This template tells earthmover what shape you want the data to be transformed to.

Create a file `templates/assessments.jsont` with the following content:

```json
{
  "assessmentIdentifier": "{{assessmentIdentifier}}",
  "assessmentTitle": "{{assessmentTitle}}",
  "namespace": "{{namespace}}",
  "assessedGradeLevels": [
    {
      "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Ninth grade"
    },
    {
      "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Tenthgrade"
    },
    {
      "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Eleventh grade"
    },
    {
      "gradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#Twelfth grade"
    }
  ],
  "assessmentCategoryDescriptor": "{{assessmentCategoryDescriptor}}",
  "academicSubjects": [
    {
      "academicSubjectDescriptor": "{{academicSubjectDescriptor}}"
    }
  ],
  "scores": [
    {
      "assessmentReportingMethodDescriptor": "uri://ea.fake.edu/assess/access/AssessmentReportingMethodDescriptor#Score",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer"
    }
  ],
  "performanceLevels": [
    {
      "assessmentReportingMethodDescriptor": "uri://ea.fake.edu/assess/access/AssessmentReportingMethodDescriptor#Performance Level",
      "performanceLevelDescriptor": "uri://ea.fake.edu/assess/access/PerformanceLevelDescriptor#High",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Level"
    },
    {
      "assessmentReportingMethodDescriptor": "uri://ea.fake.edu/assess/access/AssessmentReportingMethodDescriptor#Performance Level",
      "performanceLevelDescriptor": "uri://ea.fake.edu/assess/access/PerformanceLevelDescriptor#Medium",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Level"
    },
    {
      "assessmentReportingMethodDescriptor": "uri://ea.fake.edu/assess/access/AssessmentReportingMethodDescriptor#Performance Level",
      "performanceLevelDescriptor": "uri://ea.fake.edu/assess/access/PerformanceLevelDescriptor#Low",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Level"
    }
  ]
}
```

Notice that the shape of the template file depends on the shape required by the Ed-Fi API. Earthmover is going to take each line of the input file and create a json line using this template to form the output file.

**HINT: You can find documentation on the Ed-Fi API [here](https://api.ed-fi.org/v5.3/docs/swagger/index.html?urls.primaryName=Resources) - take note of what API version you will be posting to. For this earthmover tutorial, it doesn't really matter because we won't be pushing any data to an ODS.**

These templates incorporate jinja. The double curly braces surround {{variable names}} which correspond with column names in your input file. If you've applied any transformations in the `earthmover.yaml` - such as column renaming - then the variable names will be coming from the config instead of the original file.

## Define a destination

In your `earthmover.yaml` config file, a destination tells earthmover what data to apply a template to before writing it to your `OUTPUT_DIR`. Copy and paste the text under destinations:
```yaml
destinations:
  assessments:
    source: $sources.assessments
    template: ${BUNDLE_DIR}/templates/assessments.jsont
    extension: jsonl
```
This is telling earthmover to:

-   Take the assessments source defined earlier in the config
-   Apply the template `assessments.jsont` (which we just created)
-   Output it to the directory defined at runtime `OUTPUT_DIR`, saved with the extension `jsonl`

## Run earthmover and inspect the output

**HINT: Make sure you have a virtual environment activated with earthmover installed. You can `pip install earthmover` from pypi.**

You're now ready to run earthmover! Run the following command:

```bash
earthmover run -c earthmover.yaml -p '{
"BUNDLE_DIR": ".",
"OUTPUT_DIR": "output"}'
```

You should see a new file in your directory at `output/assessments.jsonl`. This is your transformed assessment metadata record. Open it side by side with your template and your seed file, compare and contrast to see what happened.

You're done! Congratulations on running earthmover for the first time.

# Step 4: Keep learning!

## Documentation

This tutorial was a simple example and it was not meant to show you a comprehensive view of all that earthmover can do. Earthmover has a wide variety of functionality, which are well documented in the [project README.](https://github.com/edanalytics/earthmover?tab=readme-ov-file)

## Example projects

Look through the [earthmover example projects directory](https://github.com/edanalytics/earthmover/tree/main/example_projects) for examples of different things earthmover can do. Clone the repo and try running them starting from 01_simple, comparing the inputs, config, and outputs to understand what they're doing.
