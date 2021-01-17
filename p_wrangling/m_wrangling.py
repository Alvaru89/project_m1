import pandas as pd
import requests
import json
import os
import csv

def clean_age (item):
    if "years old" in item:
        return int(item[0:2])
    elif len(item) == 4:
        return 2016 - int(item)

def importing_country_code():
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

def add_country(code,country_dict):
    return country_dict[code]


def job_dict_api(search_val):
    url = 'http://api.dataatwork.org/v1/jobs/'
    job_dict = {}
    for val in search_val:
        if val == None:
            job_dict[val] = None
        else:
            data = val
            res = requests.get(url + data)
            job_title = res.json()
            job_dict[val] = job_title['title']
    print('Job dict finished!')
    return job_dict

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

def qty_columns(raw_df):
    job_counts = dict(raw_df['Job Title'].value_counts())
    people_with_job = raw_df['Job Title'].count()

    for i in raw_df.index:
        if pd.notnull(raw_df.loc[i, 'Job Title']):
            raw_df.loc[i, 'Quantity'] = job_counts[raw_df.loc[i, 'Job Title']]
            raw_df.loc[i, 'Percentage'] = job_counts[raw_df.loc[i, 'Job Title']] * 100 / people_with_job
    return raw_df

def build_data(raw_df) -> pd.DataFrame:
    print('cleaning age')
    raw_df["Age"] = raw_df.apply(lambda x: clean_age(x["age"]), axis=1)
    print('updating age to 2020')
    raw_df['Age'] = raw_df['Age'] + 4

    print('importing country code dict')
    country_dict=importing_country_code()
    print('adding country')
    raw_df["Country"] = raw_df.apply(lambda x: add_country(x["country_code"], country_dict), axis=1)

    #getting job title
    search_val = list(raw_df['normalized_job_code'].unique())
    job_dict = create_job_dict(search_val)
    for i in raw_df.index:
        raw_df.loc[i, 'Job Title'] = job_dict[raw_df.loc[i, 'normalized_job_code']]

    #adding qty and % column
    qty_columns(raw_df)

    #dropping unnecessary columns and return

    return raw_df[['Country','Job Title','Age','Quantity','Percentage']]
