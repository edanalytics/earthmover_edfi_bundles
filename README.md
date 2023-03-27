Bundles are pre-built data mappings for converting various data formats to Ed-Fi format using [earthmover](https://github.com/edanalytics/earthmover). They consist of a folder with CSV seed data, JSON template files, and YAML configuration files for doing the transformation and sending the JSON data into an Ed-Fi API.

Data converted to the [Ed-Fi JSON standard](https://api.ed-fi.org/) can be subsequently 
loaded to Ed-Fi ODSes using [lightbeam](https://github.com/edanalytics/lightbeam),
or 

Our Earthmover bundles aim to be as complete as possible in their data coverage,
while also being portable, reusable, and flexible.


Unless otherwise noted, bundles included here have been tested with recent versions
of Ed-Fi, and recent versions of the file formats being mapped, with no known compatibilty issues.
