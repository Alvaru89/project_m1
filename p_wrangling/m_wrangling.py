import pandas as pd
import requests
import os
import json
import csv
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def clean_age (item):
    if "years old" in item:
        return int(item[0:2])
    elif len(item) == 4:
        return 2016 - int(item)

def importing_country_code_csv():
    country_equiv = pd.read_csv('data/country_code.csv', names=['Country', 'Code'])
    # Converting to dictionary
    country_dict = {}
    for i in country_equiv.index:
        k = country_equiv.loc[i, 'Code']
        v = country_equiv.loc[i, 'Country']
        country_dict[k[1:3]] = v #slicing to remove parenthesis
    # Adding missing values
    country_dict['GB'] = 'Great Britain'
    country_dict['GR'] = 'Greece'
    return country_dict

def importing_country_code_webscrap():
    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    clean_table = re.sub(r'\<.+\>', '', str(table))
    clean_string = re.sub(r'\n', '', clean_table)

    countries = re.findall(r'[A-Z][a-z]+', clean_string)
    # print(countries)

    codes = re.findall(r'[A-Z]{2}', clean_string)
    country_dict={}
    for i in range(len(codes)):
        country_dict[codes[i]]=countries[i]
    # Adding missing values
    country_dict['GB'] = 'Great Britain'
    country_dict['GR'] = 'Greece'
    return country_dict


def job_dict_api(search_val):
    url = 'http://api.dataatwork.org/v1/jobs/'
    job_dict = {}
    for val in tqdm(search_val):
        if val == None:
            job_dict[val] = None
        else:
            res = requests.get(url + val)
            job_dict[val] = res.json()['title']
    print(' ')
    print('Job dict finished!')
    return job_dict

def job_skills_dict_api(search_val):
    url = 'http://api.dataatwork.org/v1/jobs/'
    job_dict={}
    job_skills={}

    for val in tqdm(search_val):
        if val==None:
            job_dict[val]=None
            job_skills[val]=None
        else:
            try:
                res = requests.get(url+val+'/related_skills')
                job_dict[val] = res.json()['job_title']
                job_skills[val]={res.json()['skills'][i]['skill_name']:res.json()['skills'][i]['importance'] for i in range(len(res.json()['skills']))}
            except:
                res = requests.get(url+val)
                job_title=res.json()['title']
                job_dict[val] = job_title
                job_skills[val]=None
    return job_dict,job_skills


def create_job_dict(search_val):
    if os.path.exists('data/job_dict.csv'):
        with open('data/job_dict.csv', 'r') as t:
            reader = csv.reader(t)
            job_dict = {row[0]: row[1] for row in reader}
            job_dict[None] = None
    else:
        job_dict=job_dict_api(search_val)
        with open('data/job_dict.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(job_dict.items())
    return job_dict

def create_job_dict_bonus(search_val):
    if os.path.exists('data/job_dict.csv') and os.path.exists('data/job_skills.csv'):
        with open('data/job_dict.csv', 'r') as t:
            reader = csv.reader(t)
            job_dict = {row[0]: row[1] for row in reader}
            job_dict[None] = None
        with open('data/job_skills.csv', 'r') as t:
            reader = csv.reader(t)
            job_skills = {row[0]: eval(row[1]) for row in reader if row[1] != ''}
    else:
        dict_list = job_skills_dict_api(search_val)
        job_dict = dict_list[0]
        job_skills = dict_list[1]
        with open('data/job_dict.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(job_dict.items())
        with open('data/job_skills.csv', 'w') as f:
            w = csv.writer(f)
            w.writerows(job_skills.items())
    return job_dict, job_skills

def qty_columns(raw_df):
    job_counts = dict(raw_df['Job Title'].value_counts())
    people_with_job = raw_df['Job Title'].count()

    for i in tqdm(raw_df.index):
        if pd.notnull(raw_df.loc[i, 'Job Title']):
            raw_df.loc[i, 'Quantity'] = job_counts[raw_df.loc[i, 'Job Title']]
            raw_df.loc[i, 'Percentage'] = job_counts[raw_df.loc[i, 'Job Title']] * 100 / people_with_job
    return raw_df

def adding_skills_cols(bonus_df):
    #identifying lists
    skill_list = []
    #print(' ')
    for text in tqdm(bonus_df['Job Skills']):
        if text != '':
            temp_dict=eval(text)
            for skill,importance in temp_dict.items():
                if skill not in skill_list:
                    skill_list.append(skill)
    print('adding skills to dataframe...')
    bonus_df = pd.concat([bonus_df, pd.DataFrame(columns=skill_list, dtype=float)])
    print('adding importance values to dataframe...')
    for i in tqdm(bonus_df.index):
        if bonus_df.loc[i, 'Job Skills'] != '':
            temp_dict=eval(bonus_df.loc[i, 'Job Skills'])
            for skill, importance in temp_dict.items():
                bonus_df.loc[i, skill] = float(importance)
    return bonus_df

def adding_skills_cols2(bonus_df,job_skills):
    skills_df = pd.DataFrame(job_skills,dtype=float).T
    bonus_df = bonus_df.merge(skills_df, how='left', left_on='normalized_job_code', right_index=True)
    return bonus_df


def vote(x):
    if x == 'I would probably vote for it' or x == 'I would vote for it':
        return 'In Favor'

    elif x == 'I would not vote':
        return 'Neutral'

    elif x == 'I would probably vote against it' or x == 'I would vote against it':
        return 'Against'

def counter(arguments,arguments_pro, arguments_con):
    i=0
    for argument in arguments:
        if argument in arguments_pro or argument in arguments_con:
            i+=1
    return i

def build_data(raw_df) -> pd.DataFrame:
    print('cleaning age...')
    raw_df["Age"] = raw_df.apply(lambda x: clean_age(x["age"]), axis=1)
    print('updating age to 2020...')
    raw_df['Age'] = raw_df['Age'] + 4

    print('importing country code dict...')
    country_dict = importing_country_code_webscrap()
    print('adding country...')
    #raw_df["Country"] = raw_df.apply(lambda x: add_country(x["country_code"], country_dict), axis=1)
    raw_df["Country"] = raw_df.apply(lambda x: country_dict[x["country_code"]], axis=1)

    #getting job title
    print('creating dictionaries...')
    search_val = list(raw_df['normalized_job_code'].unique())
    job_dict = create_job_dict(search_val)
    print(' ')
    print('adding job titles...')
    for i in tqdm(raw_df.index):
        raw_df.loc[i, 'Job Title'] = job_dict[raw_df.loc[i, 'normalized_job_code']]
    print(' ')
    print('adding qty and % columns...')
    qty_columns(raw_df)

    #dropping unnecessary columns and return
    return raw_df[['Country','Job Title','Age','Quantity','Percentage']]

def build_data_bonus(bonus_df, bonus):
    if bonus == 1:
        #dropping unnecesary columns
        bonus_df.drop(['uuid', 'normalized_job_code', 'dem_education_level'], axis=1, inplace=True)

        print('cleaning data...')
        bonus_df['question_bbi_2016wave4_basicincome_argumentsfor'] = bonus_df.apply(
            lambda x: x['question_bbi_2016wave4_basicincome_argumentsfor'].split(' | '), axis=1)
        bonus_df['question_bbi_2016wave4_basicincome_argumentsagainst'] = bonus_df.apply(
            lambda x: x['question_bbi_2016wave4_basicincome_argumentsagainst'].split(' | '), axis=1)

        print('compiling argument lists...')
        arguments_pro = []
        for i in bonus_df.index:
            for j in bonus_df.loc[i, 'question_bbi_2016wave4_basicincome_argumentsfor']:
                if j not in arguments_pro:
                    arguments_pro.append(j)

        if 'None of the above' in arguments_pro:
            arguments_pro.remove('None of the above')

        arguments_con= []
        for i in bonus_df.index:
            for j in bonus_df.loc[i, 'question_bbi_2016wave4_basicincome_argumentsagainst']:
                if j not in arguments_con:
                    arguments_con.append(j)

        if 'None of the above' in arguments_con:
            arguments_con.remove('None of the above')

        bonus_df['Position'] = bonus_df.apply(lambda x: vote(x['question_bbi_2016wave4_basicincome_vote']), axis=1)
        bonus_df['Number of Pro arguments'] = bonus_df.apply(
            lambda x: counter(x['question_bbi_2016wave4_basicincome_argumentsfor'], arguments_pro ,arguments_con), axis=1)
        bonus_df['Number of Cons arguments'] = bonus_df.apply(
            lambda x: counter(x['question_bbi_2016wave4_basicincome_argumentsagainst'], arguments_pro ,arguments_con), axis=1)
        bonus_df['Quantity']=1
        result = bonus_df.groupby(by='Position').sum()
        return result

    if bonus == 2:
        #ignore country code and age
        #dropping unnecesary columns
        bonus_df.drop(['uuid',
                       'question_bbi_2016wave4_basicincome_argumentsfor',
                       'question_bbi_2016wave4_basicincome_argumentsagainst',
                       'question_bbi_2016wave4_basicincome_vote'], axis=1, inplace=True)

        print('creating dictionaries')
        search_val = list(bonus_df['normalized_job_code'].unique())
        dict_list = create_job_dict_bonus(search_val)
        job_dict=dict_list[0]
        job_skills=dict_list[1]
        print(' ')
        print('adding job title...')
        for i in tqdm(bonus_df.index):
            bonus_df.loc[i, 'Job Title'] = job_dict[bonus_df.loc[i, 'normalized_job_code']]
        print(' ')
        print('adding job skills...')
        #try:
         #   bonus_df['Job Skills'] = bonus_df.apply(lambda x: json.loads(job_skills[x['normalized_job_code']]), axis=1)
        #except:
         #   bonus_df['Job Skills'] = bonus_df.apply(lambda x: job_skills[x['normalized_job_code']], axis=1)

        #dropping non-relevant rows
        bonus_df.dropna(axis=0, subset=['dem_education_level'], inplace=True)
        #bonus_df.dropna(axis=0, subset=['Job Skills'], inplace=True)
        print(' ')
        print('adding skill columns...')
        bonus_df=adding_skills_cols2(bonus_df,job_skills)
        print(' ')
        print('grouping rows per education level...')
        grouped_df = bonus_df.groupby(by='dem_education_level').mean()
        top_skills_dict = {}
        for i in grouped_df.index:
            top_skills_dict[i] = grouped_df.T[i].sort_values(ascending=False)[:10]

        result=pd.DataFrame(top_skills_dict).T

        return result
