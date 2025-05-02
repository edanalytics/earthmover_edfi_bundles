import pandas as pd

def ap_pre_execute(input_file, output_file):
    """
    Processes AP assessment data by unpivoting exams and awards, joins them,
    and saves the results to CSV files.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Base path for output files.
    """
    # Load data (force all columns to string type)
    df = pd.read_csv(input_file, dtype=str, na_values='')
    df_copy = df.copy()
    
    # ---------- Unpivot Exam Data ----------
    id_columns = ['Student Identifier', 'Grade Level', 'AI Code']
    exam_ids = [f"{i:02d}" for i in range(1, 31)]  # 01 to 30
    
    unpivoted_exams = []
    for exam_id in exam_ids:
        columns = {
            'SchoolYear': f'Admin Year {exam_id}',
            'ExamCode': f'Exam Code {exam_id}',
            'Score': f'Exam Grade {exam_id}',
            'IrregularityCode1': f'Irregularity Code #1 {exam_id}',
            'IrregularityCode2': f'Irregularity Code #2 {exam_id}'
        }
        available_cols = [col for col in columns.values() if col in df_copy.columns]
        if len(available_cols) >= 3:
            subset = df_copy[id_columns + available_cols].copy()
            rename_dict = {v: k for k, v in columns.items() if v in subset.columns}
            subset.rename(columns=rename_dict, inplace=True)
            subset['Exam_Id'] = exam_id
            subset.rename(columns={
                'Student Identifier': 'studentUniqueId',
                'Grade Level': 'GradeLevel',
                'AI Code': 'SchoolCode'
            }, inplace=True)
            subset = subset[subset['studentUniqueId'].astype(str) != '']
            subset['studentUniqueId'] = subset['studentUniqueId'].astype(str)
            subset['ExamCode'] = subset['ExamCode'].astype(str)
            unpivoted_exams.append(subset)
    
    if unpivoted_exams:
        stacked_results = pd.concat(unpivoted_exams, ignore_index=True)
        # Filter out rows where both ExamCode and Score are NaN
        stacked_results = stacked_results[
            ~(stacked_results['ExamCode'].isna() | stacked_results['Score'].isna())
        ]
        stacked_results['School_Year'] = stacked_results['SchoolYear'].apply(
            lambda x: '20' + str(x) if pd.notna(x) else ''
        )
    else:
        stacked_results = pd.DataFrame(columns=['studentUniqueId', 'GradeLevel', 'SchoolCode', 
                                                'SchoolYear', 'ExamCode', 'Score', 
                                                'IrregularityCode1', 'IrregularityCode2', 
                                                'Exam_Id', 'ExamCodeValue', 'School_Year'])
    
    # ---------- Unpivot Award Data ----------
    award_ids = [str(i) for i in range(1, 7)]  # 1 to 6
    unpivoted_awards = []
    for award_id in award_ids:
        cols = {
            'AwardType': f'Award Type {award_id}',
            'AwardYear': f'Award Year {award_id}'
        }
        available_cols = [col for col in cols.values() if col in df_copy.columns]
        if len(available_cols) == 2:
            subset = df_copy[id_columns + available_cols].copy()
            rename_dict = {v: k for k, v in cols.items() if v in subset.columns}
            subset.rename(columns=rename_dict, inplace=True)
            subset['AwardType_Id'] = award_id
            subset.rename(columns={
                'Student Identifier': 'studentUniqueId',
                'Grade Level': 'GradeLevel',
                'AI Code': 'SchoolCode'
            }, inplace=True)
            subset = subset[subset['studentUniqueId'].astype(str) != '']
            subset['studentUniqueId'] = subset['studentUniqueId'].astype(str)
            subset['AwardType'] = subset['AwardType'].astype(str)
            subset['AwardYear'] = subset['AwardYear'].astype(str)
            unpivoted_awards.append(subset)
    
    if unpivoted_awards:
        stacked_awards = pd.concat(unpivoted_awards, ignore_index=True)
        # Replace non-standard missing values (e.g., 'nan', empty strings, or whitespace) with NaN
        stacked_awards['AwardType'] = stacked_awards['AwardType'].replace(['nan', ''], pd.NA, regex=False)
        # Apply the filter
        stacked_awards = stacked_awards[
            ~(stacked_awards['AwardType'].isna() | stacked_awards['AwardYear'].isna())
        ]
    else:
        stacked_awards = pd.DataFrame(columns=['studentUniqueId', 'GradeLevel', 'SchoolCode', 
                                               'AwardType', 'AwardYear', 'AwardType_Id'])
    
    # ---------- Join Awards with Exams ----------
    if stacked_results.empty or stacked_awards.empty:
        joined_data = stacked_results if not stacked_results.empty else stacked_awards if not stacked_awards.empty else pd.DataFrame()
    else:
        left_join_keys = ['studentUniqueId', 'School_Year', 'SchoolCode', 'GradeLevel']
        right_join_keys = ['studentUniqueId', 'AwardYear', 'SchoolCode', 'GradeLevel']
        
      
       
        joined_data = stacked_results.merge(
            stacked_awards,
            left_on=left_join_keys,
            right_on=right_join_keys,
            how='left',
            suffixes=('_exam', '_award')
        )
    
    
    # ---------- Save the results ----------
    stacked_results.to_csv(output_file + '_exams.csv', index=False)
    stacked_awards.to_csv(output_file + '_awards.csv', index=False)
    joined_data.to_csv(output_file, index=False)
    
    print(f"Processed joined data saved to {output_file}")
    print(f"Exam data saved to {output_file}_exams.csv")
    print(f"Award data saved to {output_file}_awards.csv")
