"""
    Script for creating NYC education database
"""

import pandas as pd
import sqlalchemy as sa

SAT_df = pd.read_csv('res/SAT_dataframe.csv')

print(SAT_df.head())

schools = SAT_df[['dbn','school_name','Boro','District','School_Num',
                    'Zip','Nhood','Latitude','Longitude']]
schools.set_index('dbn', inplace=True)

SAT_table = SAT_df[['dbn','sat_critical_reading_avg_score','sat_math_avg_score',
                    'sat_writing_avg_score','Total_1600','num_of_sat_test_takers']]
SAT_table.set_index('dbn', inplace=True)
SAT_table = SAT_table.dropna(axis = 0, thresh = 3)
print(len(SAT_table))
#print(SAT_table[4])

conn = sa.create_engine('sqlite:///db/nycedudata.db')

schools.to_sql(name='School',con=conn,if_exists='append',index=True)

conn.execute('CREATE TABLE IF NOT EXISTS SAT (\
                dbn TEXT,\
                reading INTEGER,\
                math INTEGER,\
                writing INTEGER,\
                total_rm INTEGER,\
                test_takers INTEGER,\
                PRIMARY KEY (dbn),\
                FOREIGN KEY (dbn) REFERENCES School (dbn)\
                );')

for school in SAT_table.index:
    values = (school, ) + tuple(SAT_table.loc[school])
    conn.execute('INSERT IF NOT EXISTS INTO SAT VALUES (?,?,?,?,?,?);',values)



test = conn.execute('SELECT * FROM SAT LIMIT 5;').fetchall()
print(test)
