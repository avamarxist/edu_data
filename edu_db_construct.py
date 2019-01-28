"""
    Script for creating NYC education database
"""

import pandas as pd
import json
import sqlalchemy as sa
import requests as req


"""
Construct database from original SAT data geographic data
"""

SAT_df = pd.read_csv('res/SAT_dataframe.csv')

print(SAT_df.head())

# schools = SAT_df[['dbn','school_name','Boro','District','School_Num',
#                     'Zip','Nhood','Latitude','Longitude']]
# schools.set_index('dbn', inplace=True)

SAT_table = SAT_df[['dbn','sat_critical_reading_avg_score','sat_math_avg_score',
                    'sat_writing_avg_score','Total_1600','num_of_sat_test_takers']]
SAT_table.applymap( lambda x: x.lower() if type(x)==str else x )

SAT_table = SAT_table.dropna(axis = 0, thresh = 3)
# numeric_cols = ['sat_critical_reading_avg_score','sat_math_avg_score',
#                     'sat_writing_avg_score','Total_1600','num_of_sat_test_takers']
# SAT_table[numeric_cols] = SAT_table[numeric_cols].astype(int)


print(len(SAT_table))
print(type(SAT_table['Total_1600'][4]))
#print(SAT_table[4])

conn = sa.create_engine('sqlite:///db/nycedudata.db')

conn.execute('CREATE TABLE IF NOT EXISTS SAT (\
                dbn TEXT,\
                reading NUMERIC,\
                math NUMERIC,\
                writing NUMERIC,\
                total_rm NUMERIC,\
                test_takers NUMERIC,\
                PRIMARY KEY (dbn),\
                FOREIGN KEY (dbn) REFERENCES Schools (dbn)\
                );')

for i in SAT_table.index:
    values = tuple(SAT_table.loc[i])
    conn.execute('INSERT INTO SAT VALUES (?,?,?,?,?,?);',values)


test = conn.execute('SELECT * FROM SAT LIMIT 5;').fetchall()
print(test)
