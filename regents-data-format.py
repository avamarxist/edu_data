# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:41:29 2019

@author: bahar
"""

"""
Construct table for Regents 2015-17 data
"""
import requests as req
import pandas as pd
import numpy
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sqlite

"""
create Dataframe from raw data
"""
#
# regents_raw_df = pd.read_excel('res/2015-17-NYC-Regents.xlsx')
#
# old_cols = ['School DBN','Year','Regents Exam', 'Total Tested',
#             'Demographic Category','Demographic Variable','Mean Score',
#             'Number Scoring Below 65', 'Percent Scoring Below 65',
#             'Number Scoring 65 or Above', 'Percent Scoring 65 or Above',
#             'Number Scoring 80 or Above', 'Percent Scoring 80 or Above']
#
# new_cols = ['dbn','year','exam_name', 'test_num',
#             'demo_cat','demo_var','mean_score',
#             'num_lt_65', 'pct_lt_65',
#             'num_gt_65', 'pct_gt_65',
#             'num_gt_80', 'pct_gt_80']
#
# num_cols = ['mean_score', 'num_lt_65', 'pct_lt_65','num_gt_65', 'pct_gt_65',
#             'num_gt_80', 'pct_gt_80']
#
# regents_raw_df = regents_raw_df[old_cols]
# regents_raw_df.columns = new_cols
#
# regents_df = regents_raw_df.applymap( lambda x: x.lower() if type(x) == str else x )
# regents_df = regents_df.applymap( lambda x: None if x == 's' else x )
# regents_df = regents_df.dropna(axis=0,subset=num_cols,how='all')
# regents_df = regents_df.applymap( lambda x: float(x) if type(x)==int else x)
# regents_df['demo_var'] = regents_df['demo_var'].apply( lambda x: 'other races' if x == 'multiple race categories not represented' else x)
#
# print('Dataframe size after dropna: ' + str(len(regents_df)))
#
#
# regents_df.to_csv('res/regents_cleaner.csv',index=False)


# SAT_df = pandas.read_csv('res/SAT_dataframe.csv')
# regents_names = [name.lower() for name in regents_df.drop_duplicates(subset='School Name',keep='first')['School Name']]
# sat_names = [name.lower() for name in SAT_df.drop_duplicates(subset='school_name',keep='first')['school_name']]
# print(len(regents_names))
# print(len(sat_names))
# common = set(sat_names) - (set(sat_names) - set(regents_names))
# print(len(common))
# print(set(sat_names)-common)

"""
load from csv if already cleaned
"""
regents_df = pd.read_csv('res/regents_cleaner.csv', na_values = 's')
regents_df = regents_df.applymap( lambda x: None if x == 's' else x )
regents_df = regents_df.applymap( lambda x: float(x) if type(x)==int else x)

"""
sqlite stuff
"""
engine = sa.create_engine('sqlite:///db/nycedudata.db')
#

meta = sa.MetaData()
schools_table = sa.Table('Schools',meta,autoload=True,autoload_with=engine)
# regents_table = sa.Table('Regents',meta,autoload=True,autoload_with=engine)
years_table = sa.Table('Years',meta,autoload=True,autoload_with=engine)
demo_category_table = sa.Table('Demo_Categories', meta,\
                sa.Column('demo_cat_id', sqlite.INTEGER, primary_key=True),\
                sa.Column('demo_cat', sqlite.TEXT),\
                sa.Column('demo_var', sqlite.TEXT),\
                sqlite_autoincrement=True)
demo_category_table.create(engine)
demo_pairs = list(set(zip(regents_df['demo_cat'],regents_df['demo_var'])))
values = [{'demo_cat':pair[0],'demo_var':pair[1]} for pair in demo_pairs]
engine.execute(demo_category_table.insert(),values)

# regents_table = sa.Table('Regents', meta,\
#                 sa.Column('test_id', sqlite.INTEGER, primary_key=True),\
#                 sa.Column('dbn', sqlite.TEXT,sa.ForeignKey('Schools.dbn')),\
#                 sa.Column('year', sqlite.INTEGER,sa.ForeignKey('Years.year')),\
#                 sa.Column('exam_name',sqlite.TEXT),\
#                 sa.Column('test_num', sqlite.INTEGER),\
#                 sa.Column('demo_cat', sqlite.TEXT,sa.ForeignKey('Demo_Categories.demo_cat')),\
#                 sa.Column('demo_var', sqlite.TEXT,sa.ForeignKey('Demo_Categories.demo_var')),\
#                 sa.Column('mean_score', sqlite.REAL),\
#                 sa.Column('num_lt_65', sqlite.INTEGER),\
#                 sa.Column('pct_lt_65', sqlite.REAL),\
#                 sa.Column('num_gt_65', sqlite.INTEGER),\
#                 sa.Column('pct_gt_65', sqlite.REAL),\
#                 sa.Column('num_gt_80', sqlite.INTEGER),\
#                 sa.Column('pct_gt_80', sqlite.REAL),\
#                 sqlite_autoincrement=True)
#
# regents_table.create(engine)
# ins = regents_table.insert()
# values = [dict(regents_df.loc[r]) for r in regents_df.index]
# engine.execute(ins,values)
