import pandas as pd
import re
from itertools import product

def myIGDIs_pre_exec(input_file, output_file):
    # Define assessment and window mappings
    assessment = {
        'Early Literacy+': [
            'Alliteration',
            'Picture Naming',
            'Rhyming',
            'Sound ID',
            'WODB'
        ],
        'Early Numeracy': [
            '1-to-1 Correspondence Counting',
            'Number Naming',
            'Oral Counting',
            'Quantity Comparison'
        ],
        'Español': [
            'Expressive Verbs/Verbos Expressivos',
            'First Sounds/Primeros Sonidos',
            'Letter ID/Identificación de las letras',
            'Picture Naming/Denominacion de los Dibujos',
            'Sound ID/Identificación de los sonidos'
        ],
        'ProLADR': [
            'Approaches to Learning',
            'Cognitive',
            'Creativity and the Arts',
            'Language and Literacy',
            'Physical and Motor',
            'Social and Emotional'
        ]
    }
    
    assessment_window = {
        'Early Literacy+': [
            'Fall 1', 'Fall 2', 'Fall 3', 'Fall 4', 'Fall Screening',
            'Winter 1', 'Winter 2', 'Winter 3', 'Winter 4', 'Winter Screening',
            'Spring 1', 'Spring 2', 'Spring 3', 'Spring 4', 'Spring Screening',
            'Summer 1', 'Summer 2', 'Summer 3', 'Summer 4', 'Summer Screening'
        ],
        'Early Numeracy': [
            'Fall 1', 'Fall 2', 'Fall 3', 'Fall 4', 'Fall Screening',
            'Winter 1', 'Winter 2', 'Winter 3', 'Winter 4', 'Winter Screening',
            'Spring 1', 'Spring 2', 'Spring 3', 'Spring 4', 'Spring Screening',
            'Summer 1', 'Summer 2', 'Summer 3', 'Summer 4', 'Summer Screening'
        ],
        'Español': [
            'Fall 1', 'Fall 2', 'Fall 3', 'Fall 4', 'Fall Screening',
            'Winter 1', 'Winter 2', 'Winter 3', 'Winter 4', 'Winter Screening',
            'Spring 1', 'Spring 2', 'Spring 3', 'Spring 4', 'Spring Screening',
            'Summer 1', 'Summer 2', 'Summer 3', 'Summer 4', 'Summer Screening'
        ],
        'ProLADR': [
            'Fall Screening', 'Winter Screening', 'Spring Screening', 'Summer Screening'
        ]
    }
    
    # Load the dataset
    df = pd.read_csv(input_file)
    
   
    def parse_header(column):

        # Use itertools.product to efficiently check all assessment combinations
        for assess_key, objectives in assessment.items():
            windows = assessment_window[assess_key]
            # Use product to generate all combinations of objectives and windows for this assessment
            for objective, window in product(objectives, windows):
                if objective in column and window in column:
                    base = f"{assess_key}/{objective}/{window}"
                    if column.startswith(base):
                        metric_type = column[len(base) + 1:]  # Extract part after base and '/'
                        if metric_type == 'Scaled Score' and assess_key == 'Early Literacy+':
                            metric_type = 'Score'  # Normalize Scaled Score to Score
                        return {
                            'MetricType': metric_type,
                            'Base': base
                        }
        return None
    
    # Parse headers and group columns by their prefixes
    grouped_columns = {}
    for column in df.columns:
        parsed = parse_header(column)
        if parsed:
            base = parsed['Base']
            if base not in grouped_columns:
                grouped_columns[base] = {}
            grouped_columns[base][parsed['MetricType']] = column
    
    # Prepare stacked data
    stacked_data = []
    
    for base, metrics in grouped_columns.items():
        for _, row in df.iterrows():
            stacked_row = {
                "SchoolYear": row["School Year"],
                "StateName": row["State Name"],
                "DistrictName": row["District Name"],
                "SchoolName": row["School Name"],
                "ClassroomName": row["Classroom Name"],
                "InitDistrictId": row["Init District Id"],
                "StudentId": row["Student Id"],
                "Assessment": base.split('/')[0],
                "Objective": base.split('/')[1],
                "TimeWindow": base.split('/')[2],
                "AssessmentIdentifier": f"{base.split('/')[0].replace(' ', '')}_{base.split('/')[1].replace(' ', '')}"
            }
            # Add normalized Score, Tier, and AdministrationDate (if present)
            stacked_row['Score'] = row[metrics.get('Score', '')] if 'Score' in metrics else None
            stacked_row['Tier'] = row[metrics.get('Tier', '')] if 'Tier' in metrics else None
            stacked_row['AdministrationDate'] = row[metrics.get('Date Of Administration', '')] if 'Date Of Administration' in metrics else None
            
            # Append row only if at least one metric is non-empty
            if any(pd.notna(stacked_row[key]) for key in ['Score', 'Tier', 'AdministrationDate']):
                stacked_data.append(stacked_row)
    
    # Convert stacked data to DataFrame and save to output file
    stacked_df = pd.DataFrame(stacked_data)
    
     # Keep the first occurrence if duplicates are found
    if not stacked_df.empty:
        stacked_df.drop_duplicates(subset=['StudentId', 'AssessmentIdentifier', 'AdministrationDate'], keep='first', inplace=True)
    
    stacked_df.to_csv(output_file, index=False)
    return output_file