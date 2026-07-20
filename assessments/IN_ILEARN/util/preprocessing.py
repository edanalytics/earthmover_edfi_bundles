import os
import csv
import pandas as pd
import re
 
    
def remove_col_name_special_charc(
    input_file_path,
    output_file_path,
    file_name
):
    # Sanitize file_name: remove special characters and replace spaces with underscores
    file_name = re.sub(r'[^\w\s.]', '', file_name)  # Remove special characters, ignore periods
    file_name = file_name.replace(" ", "_")       
        
    # Read headers and remove BOM
    with open(input_file_path, "r", encoding="ISO-8859-1") as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        cleaned_headers = [header.replace("®","").replace("Ã","").replace("Â","") for header in headers]
        rows = list(reader)
    
    full_path = os.path.join(output_file_path, file_name)
    os.makedirs(os.path.dirname(full_path,), exist_ok=True)
    df = pd.DataFrame(rows, columns=cleaned_headers)
    df.to_csv(full_path, header=True, index=False, encoding="utf-8", sep=",")

    return output_file_path


def ilearn_pre_exec(
    local_path: str,
    output_header_folder_name: str,
    local_download_paths: List[str],
    **context
):
    
    # Loop over files in the local_download_paths
    ts_nodash = context.get('ts_nodash')
    for local_path in local_download_paths:
                
        for file in os.listdir(local_path):
            input_file = os.path.join(local_path, file)
            # Skip directories
            if not os.path.isfile(input_file):
                continue
            
            try:
                path_parts = local_path.split(ts_nodash)
                output_file_header_fix_path = os.path.join(
                    path_parts[0], ts_nodash, output_header_folder_name,
                    *path_parts[1].lstrip("/").split("/")
                )
                output_file_path = os.path.join(
                    path_parts[0], ts_nodash, output_header_folder_name
                )
            except IndexError as e:
                print(f"Error constructing path: {e}")
                continue
            
            # Run header fix
            remove_col_name_special_charc(
                input_file_path=input_file,
                output_file_path=output_file_header_fix_path,
                file_name=file
            )

    return output_file_path