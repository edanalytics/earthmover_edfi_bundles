import json
import xmltodict
import os
import argparse

def xml_to_json(xml_path, output_path=None):
    """
    Transform an XML file into a JSON format.
    """    
    
    ### Open the input XML file and read data in form of python dictionary using xmltodict module.
    with open(xml_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
      
    ### Generate the object using json.dumps() corresponding to JSON data.
    json_data = json.dumps(data_dict)

    ### Check if output_path is provided, otherwise set it to a default value (XML folder path).
    if output_path is None:
        output_path = os.path.dirname(xml_path)
        output_directory = f'{output_path}/json'
    else:
        output_directory = f'{output_path}/json'

    ### Set the name of the json file to the name of the XML file provided.
    file_name = os.path.splitext(os.path.basename(xml_path))[0]
        
    ### Create the output directory if it doesn't exist.
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    ### Write the contents of the JSON file into the folder path with a progress bar.
    file_path = os.path.join(output_directory, f'{file_name}.json')
    with open(file_path, "w") as json_file:
        json_file.write(json_data)
        
        
if __name__ == '__main__':
    """
    This provides the command line interface to make running the script easier.

    python pre_processing.py --client-secret '{YOUR_CLIENT_SECRET}' --input ./url_list.txt --output ./ips_survey_alternative.csv
    """
    parser = argparse.ArgumentParser(
        prog="",
        description="",
        epilog=""
    )

    parser.add_argument("-i", "--xml-path",
        type=str,
        help="The XML file path including XML file name."
    )

    parser.add_argument("-o", "--output_path",
        type=str,
        help="Filepath to the output JSON file with the extracted staff data"
    )

    ### Parse and extract command-line arguments defined above.
    args = parser.parse_known_args()
    
    ### Assign command-line arguments to their corresponding variables.
    xml_path = args[0].xml_path
    output_path = args[0].output_path
    
    ### Execute main function with the variable arguments defined above.
    xml_to_json(xml_path, output_path)