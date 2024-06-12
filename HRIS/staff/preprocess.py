import json
import xmltodict

# TODO: maybe there's anice way to parameterize these, so you can call `python preprocess.py /path/to/my/file.xml`
xml_file = "/mnt/n/texas_esc_4/data/staff/lamar_cisd/STAFF/079901_000_2024FALL1_202311281227_InterchangeStaffAssociationExtension.xml"
output_folder = "/mnt/n/texas_esc_4/data/staff/lamar_cisd/STAFF/json/"

with open(xml_file) as xml_file_handle:
    # convert entire XML to a Python dict:
    data_dict = xmltodict.parse(xml_file_handle.read())
    # descend into the top-level `InterchangeStaffAssociation` key:
    if len(data_dict.keys())==1:
        data_dict = data_dict[list(data_dict.keys())[0]]
    # for the other keys (`Staff`, `PayrollExts`, etc.):
    for key in data_dict.keys():
        # make a separate JSONL file for each
        with open(f"{output_folder}{key}.jsonl", "w") as json_file:
            for item in data_dict[key]:
                # convert each item (which is a dict) to a JSON object string and write it out with a newline
                json_file.write(json.dumps(item) + "\n")