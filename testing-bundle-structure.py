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



# TODO: exceptions for the testing # FIXME: idk if I want this

class NoReadme(Exception): pass
class NoEMParams(Exception): pass



# TODO: class Checker 
class Checker:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.warnings = []
        self.successes = []
        self.not_run_tests = \
            ["Checking folder contents",
            "Getting EM parameters",
            "Compiling earthmover.yaml",
            "Checking ID package compatibility"] # FIXME: add more tests


    # TODO: checking folder contents 
    def checking_folder_contents(self):

        folder_contents = os.listdir(self.folder_path)

        required_contents = ['templates',  'lightbeam.yaml', 
            'earthmover.yaml', 'README.md', 
            'data', '_metadata.yaml', 'seeds']

        self.has_readme = 'README.md' not in folder_contents
        self.has_metadata = '_metadata.yaml' not in folder_contents


        if set(required_contents) - set(folder_contents) == set():
            self.successes.append("You seem to have all the necessary files and folders")
        else:
            missing_contents = list(set(required_contents) - set(folder_contents))
            self.warnings.append(f"You are missing the following files/folders:\n{missing_contents}")  


        if folder_contents.count("earthmover.yaml") != 1:
            self.warnings.append("Please make sure there is one earthmover.yaml file in your bundle")
        else:
            self.successes.append("There is a single earthmover.yaml file")

        if folder_contents.count("lightbeam.yaml") != 1:
            self.warnings.append("Please make sure there is one lightbeam.yaml file in your bundle")
        else:
            self.successes.append("There is a single lightbeam.yaml file")


        data_folder = os.listdir(f"{self.folder_path}/data")

        if ("sample_anonymized_file.csv" in data_folder
            or "sample_anonymized_file.txt" in data_folder):

            self.has_sample_data = True
            self.successes.append("There is a sample data file") # FIXME: there are other ways the files are named
        else:
            self.has_sample_data = False
            self.warnings.append("Missing a sample data file")

        self.not_run_tests.remove("Checking folder contents")


    # TODO: parsing readme 

    def getting_params(self):

        self.em_params = None

        readme_file_path = self.folder_path + "/README.md"

        try:
            with open(readme_file_path, "r", encoding="utf-8") as f:
                readme_file = f.read()
        except FileNotFoundError:
            raise NoReadme

        try:
            params_string = readme_file.split("earthmover run -c ./earthmover.yaml -p '")[1].split("'\n```")[0]
        except IndexError:
            params_string = readme_file.split("earthmover run -c earthmover.yaml -p '")[1].split("'\n```")[0]

        except IndexError:
            self.warnings.append("Please make sure there is a sample earthmover run command in README.md")



        # FIXME: maybe error handling for this
        try:
            em_params_dict = json.loads(params_string)
            self.em_params = json.dumps(em_params_dict)
        except:
            self.warnings.append("Unable to use provided earthmover command") # FIXME: fix it

        self.not_run_tests.remove("Getting EM parameters")




    # TODO: compiling yaml 

    def compiling_yaml(self):

        if self.em_params is None:
            raise NoEMParams

        self.em_yaml_path = self.folder_path + "/earthmover.yaml"

        command = f'''
        source ~/.venv/earthmover/bin/activate && \
        earthmover compile -c {self.em_yaml_path} -p '{self.em_params}' 
        '''
        #                                                  && \
        # earthmover run -c {self.em_yaml_path} -p '{params}'


        result = subprocess.run(
            ["bash", "-c", command],
            capture_output=True,
            text=True)

        self.warnings.append(result.stdout)
        self.warnings.append(result.stderr)

        self.not_run_tests.remove("Compiling earthmover.yaml")



    # TODO: studentAssessment.jsont 
    # FIXME: I don't know what to do with this

    def something_studentAssessment(self):

        templ_st_assess_path = f"{self.folder_path}/templates/studentAssessment.jsont"

        try:
            with open(templ_st_assess_path, "r") as f:
                self.templ_st_assess = f.read()

        except FileNotFoundError:
            templ_st_assess_path = f"{self.folder_path}/templates/studentAssessments.jsont"
            with open(templ_st_assess_path, "r") as f:
                self.templ_st_assess = f.read()

        except FileNotFoundError:
            self.warnings.append("Please make sure there is studentAssessments.jsont file in templates")


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



    # TODO parsing compiled yaml 

    def parsing_compiled_em_yaml(self):

        compiled_em_yaml_path = self.em_yaml_path[:-5] + "_compiled.yaml"

        with open(compiled_em_yaml_path, "r") as f:
            self.compiled_em_yaml_text = yaml.safe_load(f)


    # TODO check compatibility with ID package 

    def checking_id_package_compatibility(self):

        try:
            if self.compiled_em_yaml_text["transformations"]["input"] == {'source': '$sources.input', 'operations': []}:
                # print("correct transformations start")
                print()
            else:
                self.warnings.append("Please make sure the following code is in your earthmover.yaml:\
                                transformations: input: source: '$sources.input' operations: []") # FIXME: better error
        except Exception as e:
            self.warnings.append("Please make sure the following code is in your earthmover.yaml:\
                            transformations: input: source: '$sources.input' operations: []") # FIXME: better error

        try:
            if self.compiled_em_yaml_text["config"]["parameter_defaults"]["STUDENT_ID_NAME"] == "edFi_studentUniqueID":
                self.successes.append("correct default id")
            else:
                self.warnings.append('Please make sure the following code is in your earthmover.yaml:\
                                config: parameter_defaults: STUDENT_ID_NAME: "edFi_studentUniqueID"') # FIXME: better error
        except Exception as e:
            self.warnings.append('Please make sure the following code is in your earthmover.yaml:\
                            config: parameter_defaults: STUDENT_ID_NAME: "edFi_studentUniqueID"') # FIXME: better error


        self.not_run_tests.remove("Checking ID package compatibility")



    def exit_testing(self):

        print(self.not_run_tests)
        print(self.warnings)
        print(self.successes)

        # if len(not_run_tests) > 0: # FIXME: idk bro
        #     sys.exit(1)
        # else:
        #     sys.exit(0)




def main():
    
    if len(sys.argv) < 2:
        print('Usage: python testing-bundle-structure.py "<folder_path>"')
        sys.exit(1)

    folder_path = sys.argv[1]
                # "./assessments/{assessment_name}"

    c = Checker(folder_path)

    try:
        c.checking_folder_contents()
        c.getting_params()

        try:
            c.compiling_yaml()
            c.parsing_compiled_em_yaml()
            c.checking_id_package_compatibility()
        except NoEMParams:
            pass

        c.something_studentAssessment() # FIXME: this does nothing rn

    except NoReadme:
        pass

    finally:
        c.exit_testing()




if __name__ == "__main__":
    main()





"""
#     # QUESTIONS #

# # how do I know if the assessment is local (eg state-specific)

"""


















