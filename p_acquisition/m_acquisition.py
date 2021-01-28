import numpy as np
import pandas as pd
import sqlite3

def sql_con(path):
    conn = sqlite3.connect(path)
    sql_statement = '''
              SELECT personal_info.uuid,country_info.country_code, career_info.normalized_job_code, personal_info.age
              FROM personal_info
              JOIN career_info ON personal_info.uuid=career_info.uuid
              JOIN country_info ON personal_info.uuid=country_info.uuid
              JOIN poll_info ON personal_info.uuid=poll_info.uuid
              '''
    #executing sql request
    print(f'getting data from {path}')
    df=pd.DataFrame(pd.read_sql_query(sql_statement, conn))
    return df

def sql_con_bonus(path):
    conn = sqlite3.connect('data/raw_data_project_m1.db')

    sql_statement = '''
            SELECT personal_info.uuid,career_info.normalized_job_code, career_info.dem_education_level, 
            poll_info.question_bbi_2016wave4_basicincome_argumentsfor, 
            poll_info.question_bbi_2016wave4_basicincome_argumentsagainst, 
            poll_info.question_bbi_2016wave4_basicincome_vote
    
            FROM personal_info
            JOIN career_info ON personal_info.uuid=career_info.uuid
            JOIN country_info ON personal_info.uuid=country_info.uuid
            JOIN poll_info ON personal_info.uuid=poll_info.uuid
            '''
    bonus_df = pd.DataFrame(pd.read_sql_query(sql_statement, conn))
    return bonus_df

def acquire():
    #creating sql connection
    print('creating sql connection')
    path='data/raw_data_project_m1.db'
    raw_df=sql_con(path)
    print(f'{path} imported')
    return raw_df

def acquire_bonus():
    #creating sql connection
    print('creating sql connection')
    path='data/raw_data_project_m1.db'
    bonus_df=sql_con_bonus(path)
    print(f'{path} imported')
    return bonus_df