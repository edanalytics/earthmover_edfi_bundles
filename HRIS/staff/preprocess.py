import json
import xmltodict
import os

def xml_to_jsonl(xml_file_dir):
    output_path = os.path.dirname(xml_file_dir) + "/json/"

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    with open(xml_file_dir) as xml_file_handle:
        # convert entire XML to a Python dict:
        data_dict = xmltodict.parse(xml_file_handle.read())
        # descend into the top-level `InterchangeStaffAssociation` key:
        if len(data_dict.keys())==1:
            data_dict = data_dict[list(data_dict.keys())[0]]
        # for the other keys (`Staff`, `PayrollExts`, etc.):
        for key in data_dict.keys():
            # make a separate JSONL file for each
            with open(f"{output_path}{key}.jsonl", "w") as json_file:
                for item in data_dict[key]:
                    # convert each item (which is a dict) to a JSON object string and write it out with a newline
                    json_file.write(json.dumps(item) + "\n")
                
    return output_path