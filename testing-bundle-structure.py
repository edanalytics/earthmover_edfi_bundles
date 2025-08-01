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



# FIXME: bad bundles: ACCUPLACER and CogAT





# TODO: exceptions for the testing # FIXME: idk if I want this

class NoReadme(Exception): pass
class NoEMParams(Exception): pass
class InvalidBlockError(Exception): pass



# TODO: class Checker 
class Checker:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.warnings = {"Bundle Folder Contents": [], "Getting EM Parameters": [], "Compiling earthmover.yaml": [], "ID Package Compatibility": []}
        self.successes = {key: [] for key in self.warnings}


        self.not_run_tests = \
            ["Bundle Folder Contents",
            "Getting EM Parameters",
            "Compiling earthmover.yaml",
            "ID Package Compatibility"] # FIXME: add more tests


    # TODO: checking folder contents 
    def checking_folder_contents(self):

        folder_contents = os.listdir(self.folder_path)

        required_contents = ['templates',  'lightbeam.yaml', 
            'earthmover.yaml', 'README.md', 
            'data', '_metadata.yaml', 'seeds']

        self.has_readme = 'README.md' not in folder_contents
        self.has_metadata = '_metadata.yaml' not in folder_contents


        if set(required_contents) - set(folder_contents) == set():
            self.successes["Bundle Folder Contents"].append("You seem to have all the necessary files and folders at the root.\n          "+ 
                                                            "\n          ".join(f"{item}" for item in required_contents)+"\n")
        else:
            missing_contents = list(set(required_contents) - set(folder_contents))
            self.warnings["Bundle Folder Contents"].append(f"You are missing the following files/folders:\n          "+
                                                           "\n          ".join(f"{item}" for item in missing_contents)+"\n")  


        if folder_contents.count("earthmover.yaml") > 1:
            self.warnings["Bundle Folder Contents"].append(f"Please make sure there is one earthmover.yaml file in your bundle, found {folder_contents.count('earthmover.yaml')}")
        else:
            self.successes["Bundle Folder Contents"].append("There is a single earthmover.yaml file")

        if folder_contents.count("lightbeam.yaml") > 1:
            self.warnings["Bundle Folder Contents"].append(f"Please make sure there is one lightbeam.yaml file in your bundle, found {folder_contents.count('lightbeam.yaml')}")
        else:
            self.successes["Bundle Folder Contents"].append("There is a single lightbeam.yaml file")


        self.has_sample_data = False

        if "data" in folder_contents:
            data_folder = [f for f in os.listdir(f"{self.folder_path}/data")
                            if f != ".gitkeep"]

        if data_folder:
            self.has_sample_data = True
            self.successes["Bundle Folder Contents"].append("Found the following sample data files:\n          " +
                                                            "\n          ".join(file for file in data_folder))
        
        if not self.has_sample_data:
            self.warnings["Bundle Folder Contents"].append("Missing a sample data file")


        self.not_run_tests.remove("Bundle Folder Contents")


    # TODO: parsing readme 

    def getting_params(self):

        self.em_params = None

        readme_file_path = self.folder_path + "/README.md"

        try:
            with open(readme_file_path, "r", encoding="utf-8") as f:
                readme_file = f.read()
        except FileNotFoundError:
            raise NoReadme

        for pattern in ["./earthmover.yaml", "earthmover.yaml"]:
            try:
                params_string = readme_file.split(f"earthmover run -c {pattern} -p '")[1].split("'\n```")[0]
                self.successes["Getting EM Parameters"].append("Found sample Earthmover run command in the README.md")
                break
            except IndexError:
                continue
        else:
            self.warnings["Getting EM Parameters"].append("Please make sure there is a sample Earthmover run command in README.md")



        # FIXME: maybe better error handling for this
        try:
            em_params_dict = json.loads(params_string)
            self.em_params = json.dumps(em_params_dict)
            self.successes["Getting EM Parameters"].append("The Earthmover command is valid JSON")
        except json.JSONDecodeError:
            self.warnings["Getting EM Parameters"].append("Unable to use the provided earthmover command, invalid JSON: ", params_string) 

        self.not_run_tests.remove("Getting EM Parameters")




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

        if result.returncode == 0:
            self.successes["Compiling earthmover.yaml"].append("Successfully compiled with Earthmover")
        else:
            self.warnings["Compiling earthmover.yaml"].append(f"Error during compiling with Earthmover:\n{result.stdout}\n{result.stderr}")

        self.not_run_tests.remove("Compiling earthmover.yaml")



    # TODO: studentAssessment.jsont 
    def something_studentAssessment(self):
    # FIXME: useless, not running it
    # FIXME: I don't know what to do with this

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
                self.successes["ID Package Compatibility"].append("Correct transformations.input")
            else:
                raise InvalidBlockError
        except (KeyError, InvalidBlockError):
            self.warnings["ID Package Compatibility"].append("Please make sure the following block is in your `earthmover.yaml`:\n\n"
                                                                "transformations:\n"
                                                                "  input:\n"
                                                                "    source: '$sources.input'\n"
                                                                "    operations: []")


        try:
            if self.compiled_em_yaml_text["config"]["parameter_defaults"]["STUDENT_ID_NAME"] == "edFi_studentUniqueID":
                self.successes["ID Package Compatibility"].append("Correct config.parameter_defaults.STUDENT_ID_NAME")
            else:
                raise InvalidBlockError
        except (KeyError, InvalidBlockError):
            self.warnings["ID Package Compatibility"].append("Please make sure the following block is in your `earthmover.yaml`:\n\n"
                                                                "config:\n"
                                                                "  parameter_defaults:\n"
                                                                '    STUDENT_ID_NAME: "edFi_studentUniqueID"')
                

        self.not_run_tests.remove("ID Package Compatibility")


    # TODO: exit testing
    def exit_testing(self):

        """✨ ⚠️ ✅"""


        for key in self.warnings.keys():
            if key in self.not_run_tests:
                continue

            print(f"\n✨ {key}")

            for warning in self.warnings[key]:
                print(f"    ⚠️  {warning}")

            for success in self.successes[key]:
                print(f"    ✅ {success}")


        if len(self.not_run_tests) > 0:
            print("\n⚠️  Not run tests:")
            for test in self.not_run_tests:
                print(f"        {test}")

        print()


def main():
    
    if len(sys.argv) < 2:
        print('Usage: python testing-bundle-structure.py <folder_path>')
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

        # c.something_studentAssessment() # FIXME: this does nothing rn

    except NoReadme:
        pass

    finally:
        c.exit_testing()

        if os.path.exists(os.path.join(folder_path, "earthmover_compiled.yaml")):
            os.remove(os.path.join(folder_path, "earthmover_compiled.yaml"))





if __name__ == "__main__":
    main()





"""
#     # QUESTIONS #

# # how do I know if the assessment is local (eg state-specific)

"""


















