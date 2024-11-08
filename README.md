Bundles are pre-built data mappings for converting various data formats to Ed-Fi format using [earthmover](https://github.com/edanalytics/earthmover). They consist of a folder with CSV seed data, JSON template files, and YAML configuration files for doing the transformation and sending the JSON data into an Ed-Fi API.

Data converted to the [Ed-Fi JSON standard](https://api.ed-fi.org/) can be subsequently 
loaded to Ed-Fi ODSes using [lightbeam](https://github.com/edanalytics/lightbeam), or sideloaded directly into an [edu](https://enabledataunion.org/) database.

Our earthmover bundles aim to be as complete as possible in their data coverage,
while also being portable, reusable, and flexible.

### Assessment Integrations
While earthmover bundles can be written for any domain of Ed-Fi, the current most common use-case is the assessment domain, because most assessment vendors do not maintain native integrations into Ed-Fi.  

To better address student matching issues when implementing these bundles on real student data, this repository includes two packages that automatically detect the correct student ID configuration to maximize student matching given an Ed-Fi roster source.

For more in-depth documentation on Ed-Fi assessment integrations, please see [this link](https://edanalytics.slite.page/p/CxcM2foMcOuk1m/Ed-Fi-Assessment-Integrations-using-earthmover-and-lightbeam-Documentation).

### Coming Soon
The next version of the bundles repository will include:
1. Breaking changes to the data model for some assessments in order to match [governance standards](https://edanalytics.slite.page/p/FwwhB84DoYVjY1/Assessment-Data-Governance-in-Ed-Fi). 
2. Updates to all of our assessment bundles to be fully compatible with Ed-Fi Data Standards [4](https://edfi.atlassian.net/wiki/spaces/EFDS4X/overview) & [5](https://edfi.atlassian.net/wiki/spaces/EFDS5/overview).