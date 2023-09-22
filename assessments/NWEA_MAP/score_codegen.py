import csv 
#Projected Proficiency Level,"Projected proficiency level on another assessment based on a linking study"
methods = []
with open('./assessments/NWEA_Map/seeds/assessmentReportingMethodDescriptors.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        methods.append(row)

# score template for studentAssessment.jsont
score_template = """
      {{% if {column_name} is not none and {column_name} | length %}}
        {{% set _ = scores.append([{column_name}, '{codeValue}', '{data_type}']) %}}
      {{% endif %}}
"""

# score template for assessments.jsont
score_template2 = """
    {{
      "assessmentReportingMethodDescriptor": "uri://www.nwea.org/map/AssessmentReportingMethodDescriptor#{codeValue}",
      "resultDatatypeTypeDescriptor": "uri://ed-fi.org/ResultDatatypeTypeDescriptor#{data_type}"
    }},
"""



scores = [score_template.format(**row) for row in methods if row['score_or_performance'] == 'score']

print(''.join(scores))

scores2 = [score_template2.format(**row) for row in methods if row['score_or_performance'] == 'score' and row['is_deprecated'] == 'False']
print(''.join(scores2))


pl_template = """
      {{% if {column_name} is not none and {column_name} | length %}}
        {{% set _ = perf_levels.append([{column_name}, '{codeValue}']) %}}
      {{% endif %}}

"""
pl = [pl_template.format(**row) for row in methods if row['score_or_performance'] == 'performance']

print(''.join(pl))

[row['codeValue'] for row in methods if row['score_or_performance'] == 'performance']