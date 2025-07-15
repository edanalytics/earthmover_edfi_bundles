import yaml
import subprocess
import os
import json
import sys
from pprint import pprint


"""
Inconsistencies:

earthmover run -c ./earthmover.yaml 
                  earthmover.yaml


templates/studentAssessment.jsont
         /studentAssessments.jsont

"""


# TODO: checking folder contents 

def checking_folder_contents(folder_path):

    has_metadata = True
    has_readme = True
    has_sample_data = True
    warnings = []

    folder_contents = os.listdir(folder_path)

    required_contents = ['templates',  'lightbeam.yaml', 
        'earthmover.yaml', 'README.md', 
        'data', '_metadata.yaml', 'seeds']


    if set(required_contents) - set(folder_contents) == set():
        print("You seem to have all the necessary files and folders")
    else:

        missing_contents = list(set(required_contents) - set(folder_contents))

        if "README.md" in missing_contents:
            has_readme = False

        if '_metadata.yaml' in missing_contents:
            has_metadata = False

        warnings.append(f"You are missing the following files/folders:\n{missing_contents}")  



    if folder_contents.count("earthmover.yaml") != 1:
        warnings.append("Please make sure there is one earthmover.yaml file in your bundle")
    # else:
    #     print("You have a single earthmover.yaml file")

    if folder_contents.count("lightbeam.yaml") != 1:
        warnings.append("Please make sure there is one lightbeam.yaml file in your bundle")
    # else:
    #     print("You have a single lightbeam.yaml file")


    data_folder = os.listdir(f"{folder_path}/data")

    if ("sample_anonymized_file.csv" in data_folder
        or "sample_anonymized_file.txt" in data_folder):

        #print("Yes sample file")
        print()
    else:
        has_sample_data = False
        warnings.append("Missing sample data file")

    return has_metadata, has_readme, has_sample_data, warnings



# TODO: parsing readme 

def getting_params(folder_path):

    warnings = []

    readme_file_path = folder_path + "/README.md"

    with open(readme_file_path, "r", encoding="utf-8") as f:
        readme_file = f.read()


    try:
        params_string = readme_file.split("earthmover run -c ./earthmover.yaml -p '")[1].split("'\n```")[0]
    except IndexError:
        params_string = readme_file.split("earthmover run -c earthmover.yaml -p '")[1].split("'\n```")[0]

    except IndexError:
        warnings.append("Please make sure there is a sample earthmover run command in README.md")

        return None, warnings


    # FIXME: maybe error handling for this
    params_dict = json.loads(params_string)

    params = json.dumps(params_dict)

    return params, warnings



# TODO: compiling yaml 

def compiling_yaml(folder_path, params):

    warnings = []

    em_yaml_path = folder_path + "/earthmover.yaml"

    command = f'''
    source ~/.venv/earthmover/bin/activate && \
    earthmover compile -c {em_yaml_path} -p '{params}' 
    '''
    #                                                  && \
    # earthmover run -c {em_yaml_path} -p '{params}'


    result = subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True)

    warnings.append(result.stdout)
    warnings.append(result.stderr)

    return em_yaml_path, warnings



# TODO: studentAssessment.jsont 
# FIXME: I don't know what to do with this

def something_studentAssessment(folder_path):

    warnings = []

    templ_st_assess_path = f"{folder_path}/templates/studentAssessment.jsont"

    try:
        with open(templ_st_assess_path, "r") as f:
            templ_st_assess = f.read()

    except FileNotFoundError:
        templ_st_assess_path = f"{folder_path}/templates/studentAssessments.jsont"
        with open(templ_st_assess_path, "r") as f:
            templ_st_assess = f.read()

    except FileNotFoundError:
        warnings.append("Please make sure there is studentAssessments.jsont file in templates")

    return templ_st_assess, warnings


"""
We need something reallyyyyy close to this





from PSAT_SAT

same code in {"studentObjectiveAssessments": [...{"score_results": [....
        and in {"scoreResults": [....

74 -----
{%- for score in all_scores -%}
      {
            "assessmentReportingMethodDescriptor": "{{namespace}}/AssessmentReportingMethodDescriptor#{{score[0]}}",
            "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer",
            "result": "{{score[1]}}"
      }
      {%- if not loop.last -%},
      {%- else %}{% endif %}{%- endfor -%}
    ],

177 -------
    "scoreResults": [
    {%- for score in all_score_obj -%}
    {
    "assessmentReportingMethodDescriptor": "{{namespace}}/AssessmentReportingMethodDescriptor#{{score[0]}}",
    "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#Integer",
    "result": "{{score[1]}}"
    }
    {%- if not loop.last -%},
    {%- else %}{% endif %}{%- endfor -%}
]



"""






# check for the templates NOT hard-coding descriptor namespaces
# -> under templates
# -> parse jsont
        # bottom of page 2



# check json files to make sure they are valid
# -> commas, formatting



# TODO: getting namespace from not compiled yaml 
# FIXME: gonna kill this code

"""
with open(em_yaml_path, "r") as f:
    em_yaml_text = f.read()

# print(em_yaml_text)

try:
    namespace = em_yaml_text.split('namespace: ')[1].split("\n")[0]
except Exception as e:
    namespace = "I failed to get the namespace"

print(namespace)
"""






# TODO parsing compiled yaml 

def parsing_compiled_em_yaml(em_yaml_path):

    compiled_em_yaml_path = em_yaml_path[:-5] + "_compiled.yaml"

    with open(compiled_em_yaml_path, "r") as f:
        compiled_em_yaml_text = yaml.safe_load(f)

    return compiled_em_yaml_text


# TODO check compatibility with ID package 

def checking_id_package_compatibility(compiled_em_yaml_text):

    warnings = []

    try:
        if compiled_em_yaml_text["transformations"]["input"] == {'source': '$sources.input', 'operations': []}:
            # print("correct transformations start")
            print()
        else:
            warnings.append("Please make sure the following code is in your earthmover.yaml:\
                            transformations: input: source: '$sources.input' operations: []") # FIXME: better error
    except Exception as e:
        warnings.append("Please make sure the following code is in your earthmover.yaml:\
                        transformations: input: source: '$sources.input' operations: []") # FIXME: better error

    try:
        if compiled_em_yaml_text["config"]["parameter_defaults"]["STUDENT_ID_NAME"] == "edFi_studentUniqueID":
            # print("correct default id")
            print()
        else:
            warnings.append('Please make sure the following code is in your earthmover.yaml:\
                            config: parameter_defaults: STUDENT_ID_NAME: "edFi_studentUniqueID"') # FIXME: better error
    except Exception as e:
        warnings.append('Please make sure the following code is in your earthmover.yaml:\
                        config: parameter_defaults: STUDENT_ID_NAME: "edFi_studentUniqueID"') # FIXME: better error

    return warnings




def exit_testing(global_warnings, not_run_tests):

    print(not_run_tests)
    print(global_warnings)

    if len(not_run_tests) > 0:
        sys.exit(1)
    else:
        sys.exit(0)




def main():

    # maybe start with all the tests in not_run_tests and then remove?

    not_run_tests = ["Checking folder contents", "Compiling earthmover.yaml",
                      "Checking ID package compatibility", "", ""]

    global_warnings = []

    if len(sys.argv) < 2:
        print('Usage: python testing-bundle-structure.py "<folder_path>"')
        sys.exit(1)

    folder_path = sys.argv[1]
                # "./assessments/{assessment_name}"

    has_metadata, has_readme, has_sample_data, folder_contents_warnings \
        = checking_folder_contents(folder_path)

    global_warnings.extend(folder_contents_warnings)
    not_run_tests.remove("Checking folder contents")


    if has_readme:
        params, readme_warnings = getting_params(folder_path)
        global_warnings.extend(readme_warnings)

    else:
        exit_testing(global_warnings, not_run_tests)


    if params is not None:
        em_yaml_path, compiling_yaml_warnings = compiling_yaml(folder_path, params)

        not_run_tests.remove("Compiling earthmover.yaml")
        global_warnings.extend(compiling_yaml_warnings)

    else:
        exit_testing(global_warnings, not_run_tests)


    compiled_em_yaml_text = parsing_compiled_em_yaml(em_yaml_path)

    id_package_warnings = checking_id_package_compatibility(compiled_em_yaml_text)

    not_run_tests.remove("Checking ID package compatibility")
    global_warnings.extend(id_package_warnings)

    templ_st_assess, st_assess_warnings = something_studentAssessment(folder_path)

    global_warnings.extend(st_assess_warnings)

    exit_testing(global_warnings, not_run_tests)



if __name__ == "__main__":
    main()





"""
#     # QUESTIONS #

# # how do I know if the assessment is local (eg state-specific)

"""


















