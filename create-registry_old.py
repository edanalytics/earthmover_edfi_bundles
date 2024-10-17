from pprint import pprint
import sys

from yaml import safe_load

path = sys.argv[1]
md = {}

# TODO: update to find all instances
with open(path) as stream:
    md = safe_load(stream)

#pprint(md)

INPUT_PARAM_KEYS = ["display_name", "is_required", "allowed_values", "default_value", "hardwire_value"]
INPUT_FILE_KEYS = ["display_name", "description", "is_required", "file_type", "header_rows"]

all_assessments = []

def match_by_env_var(lst, elem):
    return next((x for x in lst if x["env_var"] == elem["env_var"]), None)

# TODO: add note about how the traversal works, it's a little unintuitive
def add_assessments(metadata):
    if "assessments" not in metadata:
        # "leaf" case - this is a distinct assessment
        all_assessments.append(metadata)
        return

    for assessment in metadata["assessments"]:
       # print(f'before: {assessment["display_name"]}')
        if len(assessment["display_name"]) > 0:
            # TODO: could add a keyerror check with specific message here - because this would be an error in teh metadata file
            assessment["display_name"] = metadata["display_name"] + " " + assessment["display_name"] 
        else:
            assessment["display_name"] = metadata["display_name"]
        
       # print(f'after: {assessment["display_name"]}')

        if "valid_edfi" not in assessment and "valid_edfi" in metadata:
            assessment["valid_edfi"] = metadata["valid_edfi"]

        if "valid_years" not in assessment and "valid_years" in metadata:
            assessment["valid_years"] = metadata["valid_years"]

        # INPUT PARAMS - Cases to handle here (not all mutually exclusive):
        #   0. (automatic) Assessment has input params that parent doesn't have - include these unaltered
        #   1. Assessment doesn't have any input params - inherit all from parent
        #   2. Assessment has params that exist in the parent - inherit keys that exist in parent but not in assessment
        #   3. Parent has params that do not exist in the assessment - inherit from parent

        # case 1
        if "input_params" not in assessment and "input_params" in metadata:
            assessment["input_params"] = metadata["input_params"]
        else:
            # case 2
            for i, child_param in enumerate(assessment["input_params"]):
                parent_param = match_by_env_var(metadata["input_params"], child_param)
                if parent_param is not None:
                    for key in INPUT_PARAM_KEYS:
                        if key not in child_param and key in parent_param:
                            assessment["input_params"][i][key] = parent_param[key]

            # case 3
            for parent_param in metadata["input_params"]:
                if match_by_env_var(assessment["input_params"], parent_param) is None:
                    assessment["input_params"].append(parent_param)

        # INPUT FILES - cases to handle here:
        #   0. (automatic) Assessment has input files that parent doesn't have - include these unaltered
        #   1. Assessment doesn't have any input files - inherit all from parent
        #   2. Assessment has files that exist in the parent - inherit keys that exist in parent but not in assessment
        #   3. Parent has files that do not exist in the assessment - inherit from parent

        # case 1 - note that input_files is required so we don't have to check it 
        #       # TODO: or we can check for a validation error
        if "input_files" not in assessment:
            assessment["input_files"] = metadata["input_files"]
        else:
            # case 2
            for i, child_file in enumerate(assessment["input_files"]):
                parent_file = match_by_env_var(metadata["input_files"], child_file)
                if parent_file is not None:
                    for key in INPUT_FILE_KEYS:
                        if key not in child_file and key in parent_file:
                            assessment["input_files"][i][key] = parent_file[key]

                    # special additional behavior for files where we concatonate required cols
                    if len(child_file["required_cols"]) > 0:
                        # TODO: again potential for a validation error here
                        assessment["input_files"][i]["required_cols"].extend(parent_file["required_cols"])
                    else:
                        assessment["input_files"][i]["required_cols"] = parent_file["required_cols"]

            # case 3
            for parent_file in metadata["input_files"]:
                if match_by_env_var(assessment["input_files"], parent_file) is None:
                    assessment["input_files"].append(parent_file)

        add_assessments(assessment)


add_assessments(md)

pprint(all_assessments)

"""
Okay, what's the plan

1. Start with an empty list of assesssments
2. If the file doesn't have any, then populate a single one with global_meta
3. Otherwise do a depth-first search down the tree, hanging onto the 'current' values of any fields and overwriting / appending as needed
    I really hope this doesn't encourage recursion but it might...

TODO: add repo name (arg), branch name (arg), and file path

"""

"""
Here's a place to put rules

input_params


"""