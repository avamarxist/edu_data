# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:41:29 2019

@author: bahar
"""

"""
Construct table for Regents 2015-17 data
"""
import requests as req
import pandas
import sqlalchemy as sa

# json_url = "https://data.cityofnewyork.us/resource/eqwn-dfwq.json"
# json_req = req.get(json_url)
#
# regents_dict = json_req.json()

# regents_dict =
#
# print(type(regents_dict))
# print(regents_dict[1])
# print(regents_dict[1].keys())
# print(regents_dict[1].values())

regents_raw_df = pandas.read_excel('res/2015-17-NYC-Regents.xlsx')

new_cols = ['School DBN','School Name','Year','Regents Exam', 'Total Tested',
            'Demographic Category','Demographic Variable','Mean Score',
            'Number Scoring Below 65', 'Percent Scoring Below 65',
            'Number Scoring 65 or Above', 'Percent Scoring 65 or Above',
            'Number Scoring 80 or Above', 'Percent Scoring 80 or Above']

regents_raw_df = regents_raw_df[new_cols]
print(regents_raw_df.columns)
print('Size of dataframe: {}'.format(len(regents_raw_df)))

regents_df = regents_raw_df.applymap( lambda x: x.lower() if type(x) == str else x )
print('Size of dataframe: {}'.format(len(regents_df)))

# regents_df.applymap( lambda x: 'NULL' if x == 's' else x )
# print('Size of dataframe: {}'.format(len(regents_df)))

# score_df = regents_df.loc[regents_df['Mean Score'] == 's']
# print(score_df.head())
# print(score_df.tail())
# print('Size of dataframe: {}'.format(len(score_df)))

regents_df.to_csv('res/regents_cleaner.csv')
# SAT_df = pandas.read_csv('res/SAT_dataframe.csv')
#
# regents_names = [name.lower() for name in regents_df.drop_duplicates(subset='School Name',keep='first')['School Name']]
# sat_names = [name.lower() for name in SAT_df.drop_duplicates(subset='school_name',keep='first')['school_name']]
# print(len(regents_names))
# print(len(sat_names))
# common = set(sat_names) - (set(sat_names) - set(regents_names))
# print(len(common))
# print(set(sat_names)-common)

# conn = sa.create_engine('sqlite:///db/nycedudata.db')
#
# conn.execute('CREATE TABLE IF NOT EXISTS Regents (\
#                 test_id INTEGER PRIMARY KEY AUTOINCREMENT,\
#                 dbn TEXT,\
#                 school_name TEXT,\
#                 school_level TEXT,\
#                 year NUMERIC,\
#                 total_tested NUMERIC,\
#                 demo_category TEXT,\
#                 demo_variable TEXT,\
#                 mean_score NUMERIC,\
#                 num_lt_65 NUMERIC,\
#                 pct_lt_65 NUMERIC,\
#                 num_gt_65 NUMERIC,\
#                 pct_gt_65 NUMERIC,\
#                 num_gt_80 NUMERIC,\
#                 pct_gt_80 NUMERIC,\
#                 FOREIGN KEY (dbn) REFERENCES Schools (dbn),\
#                 FOREIGN KEY (school_name) REFERENCES Schools (school_name)\
#                 );')
#
# for r in regents_df.index:
#     values = ('NULL', ) + tuple(regents_df.loc[r])
#     conn.execute('INSERT INTO Regents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',values)
