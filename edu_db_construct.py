"""
    Script for creating NYC education database
"""

import pandas as pd
import sqlite3

SAT_df = pd.read_csv('res/SAT_dataframe.csv')

print(SAT_df.head())

schools = SAT_df[['dbn','school_name','Boro','District','School_Num','Zip','Nhood','Latitude','Longitude']]
print(schools.head())

schools_set = set(schools['Boro'])
print(schools_set)

"""
conn = sqlite3.connect('db/nycedudata.db')

cur = conn.cursor()

schools.to_sql(name='School',con=conn)

test = conn.execute('SELECT * FROM School LIMIT 5;').fetchall()
print(test)
"""
