"""
Format 2013-2018 school demographic data and import to sqlite database
"""

import requests as req
import pandas as pd
import numpy
import sqlalchemy as sa
import sqlalchemy.dialects.sqlite as sqlite

"""
function definitions
"""
# def normalize_df(df,cols_in,rep1,rep2):
#     table_out = []
#     for i in df.index:
#         for c in cols_in:
#             row_in = demo_df.loc[i]
#             del_cols = [col for col in cols_in if col != c]
#             keep_cols = [col for col in df.columns if col not in del_cols]
#             row_out = row_in[keep_cols]
#             row_out = list(row_out)
#             table_out.append(row_out)
#     dummy1 = cols_in[-2]
#     dummy2 = cols_in[-1]
#     cols_in = cols_in[:-2]
#     norm_cols = [ col for col in df.columns if col not in cols_in ]
#     df_norm = pd.DataFrame(table_out,columns = norm_cols)
#     df_norm = df_norm.rename(columns={dummy1:rep1,dummy2:rep2})
#
#     return df_norm

# """
# load, clean, normalize, and export cleaned data for upload to sqlite
# """
#
# demo_raw_df = pd.read_csv('res/2013_-_2018_Demographic_Snapshot_School_raw.csv')
# print('Raw size: ' + str(len(demo_raw_df)))
#
# """
# clean data
# """
#
# new_cols = [ col.lower() for col in demo_raw_df.columns ]
# new_cols = [ col.replace(' ','_') for col in new_cols ]
# new_cols = [ col.replace('#','num') for col in new_cols ]
# new_cols = [ col.replace('%','pct') for col in new_cols ]
# demo_raw_df.columns = new_cols
#
# demo_df = demo_raw_df.applymap( lambda x: x.lower() if type(x)==str else x )
# demo_df = demo_df.applymap( lambda x: float(x) if type(x)==int else x )
# demo_df = demo_df.applymap( lambda x: None if x=='no data' else x )
# demo_df['year'] = demo_df['year'].apply( lambda y: int(y.split('-')[0]) + 1 )
# demo_df['economic_need_index'] = demo_df['economic_need_index'].apply( lambda x: float(str(x).replace('%','')) if type(x)==str else x)
#
# print('Clean size: ' + str(len(demo_df)))
#
#
# demo_df = demo_df.rename(columns = \
#     {'grade_pk_(half_day_&_full_day)':'grade_pk',\
#     'num_multiple_race_categories_not_represented':'num_other_race',\
#     'pct_multiple_race_categories_not_represented':'pct_other_race',\
#     'num_students_with_disabilities':'num_swd',\
#     'pct_students_with_disabilities':'pct_swd',\
#     'num_english_language_learners':'num_ell',\
#     'pct_english_language_learners':'pct_ell'})
# demo_df = demo_df.drop(['school_name','pct_female','pct_male',
#                         'pct_asian','pct_black','pct_hispanic',
#                         'pct_other_race','pct_white','pct_swd',
#                         'pct_ell','pct_poverty'],1)
#
# demo_df.to_csv(path_or_buf='res/demo_cleaned.csv',sep='|',index=False)

# """
# normalize dataframe so that grade columns are turned into multiple rows and
# 1 column, and export
# """
# demo_df = pd.read_csv('res/demo_cleaned.csv', sep = '|', dtype={'economic_need_index':'float'})
#
# cat_dict = {}
# for col in demo_df.columns[3:17]:
#     cat_dict[col]='grade level'
# for col in demo_df.columns[17:19]:
#     cat_dict[col]='gender'
# for col in demo_df.columns[19:24]:
#     cat_dict[col]='ethnicity'
# for col in demo_df.columns[24:26]:
#     cat_dict[col]='swd status'
# for col in demo_df.columns[26:28]:
#     cat_dict[col]='ell status'
# for col in demo_df.columns[28:]:
#     cat_dict[col]='economic status'
#
#
# table_out = []
# col_sep = 3
# const_cols = demo_df.columns[0:3]
# for i in demo_df.index:
#     for col in demo_df.columns[3:17]:
#         row_out = list(demo_df[const_cols].loc[i])
#         row_out.append('grade level')
#         row_out.append(col.replace('_',' '))
#         row_out.append(demo_df[col][i])
#         row_out.append(demo_df[col][i]/demo_df['total_enrollment'][i]*100.)
#         table_out.append(row_out)
#     for col in demo_df.columns[17:]:
#         row_out = list(demo_df[const_cols].loc[i])
#         row_out.append(cat_dict[col])
#         row_out.append(col[4:].replace('_',' '))
#         row_out.append(demo_df[col][i])
#         row_out.append(demo_df[col][i]/demo_df['total_enrollment'][i]*100.)
#         table_out.append(row_out)
#
# norm_cols = list(const_cols)
# norm_cols += ['demo_cat','demo_var','demo_num','demo_pct']
#
# demo_df_norm = pd.DataFrame(table_out,columns = norm_cols)
#
# demo_df_norm.to_csv(path_or_buf='res/demo_norm.csv', sep = '|',index=False)

"""
sql stuff
"""

demo_df = pd.read_csv('res/demo_norm.csv', sep = '|', dtype={'economic_need_index':'float'})
demo_df['year'] = demo_df['year'].apply( lambda x: float(x) if type(x)==int else x )
engine = sa.create_engine('sqlite:///db/nycedudata.db')

meta = sa.MetaData()
schools_table = sa.Table('Schools',meta,autoload=True,autoload_with=engine)
regents_table = sa.Table('Regents',meta,autoload=True,autoload_with=engine)
demo_cat_table = sa.Table('Demo_Categories',meta,autoload=True,autoload_with=engine)
demographics_table = sa.Table('Demographics', meta,\
                sa.Column('demo_id', sqlite.INTEGER, primary_key=True),\
                sa.Column('dbn', sqlite.TEXT,sa.ForeignKey('Schools.dbn',onupdate='CASCADE',ondelete='SET NULL')),\
                sa.Column('year', sqlite.INTEGER,sa.ForeignKey('Years.year',onupdate='CASCADE',ondelete='SET NULL')),\
                sa.Column('total_enrollment',sqlite.TEXT),\
                sa.Column('demo_cat',sqlite.TEXT),\
                sa.Column('demo_var',sqlite.TEXT),\
                sa.Column('demo_num',sqlite.INTEGER),\
                sa.Column('demo_pct',sqlite.REAL),\
                sa.ForeignKeyConstraint(['demo_cat','demo_var'],['Demo_Categories.demo_cat','Demo_Categories.demo_var'],onupdate='CASCADE',ondelete='SET NULL'),\
                sqlite_autoincrement=True)
demographics_table.create(engine)
ins = demographics_table.insert()
values = [dict(demo_df.loc[r]) for r in demo_df.index]
engine.execute(ins,values)
