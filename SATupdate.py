import pandas as pd 
import numpy as np
import sqlalchemy as sa 

#### Load 2012 data

SAT_2010 = pd.read_json("https://data.cityofnewyork.us/resource/rt5r-ie69.json")
SAT_2012 = pd.read_json("https://data.cityofnewyork.us/resource/f9bf-2cp4.json")

SAT_2010 = SAT_2010.applymap( lambda x: x.lower() if type(x)==str else x )
SAT_2012 = SAT_2012.applymap( lambda x: x.lower() if type(x)==str else x )


SAT_2010.columns = ['reading', 'dbn', 'math', 'test_takers', 'name', 'writing']
SAT_2010['school_year'] = 2010 
SAT_2012.columns = ['dbn', 'test_takers', 'reading', 'math', 'writing', 'name']
SAT_2012['school_year'] = 2012    

numeric_cols = ['test_takers', 'reading', 'math', 'writing','school_year']
for col in numeric_cols:
    SAT_2010[col] = SAT_2010[col].apply(pd.to_numeric,args=('coerce',))
    SAT_2012[col] = SAT_2012[col].apply(pd.to_numeric,args=('coerce',))

SAT_2010['total_rm'] = SAT_2010.apply(lambda x: x['reading']+x['math'], axis=1)
SAT_2012['total_rm'] = SAT_2012.apply(lambda x: x['reading']+x['math'], axis=1)

new_cols = ['dbn', 'school_year', 'test_takers', 'reading', 'math', 'writing', 'total_rm']
SAT_2010 = SAT_2010[new_cols]
SAT_2012 = SAT_2012[new_cols]

SAT_2010['school_year'] = SAT_2010['school_year'].astype(np.float64)
SAT_2012['school_year'] = SAT_2012['school_year'].astype(np.float64)

SAT = pd.concat([SAT_2010,SAT_2012], ignore_index=True)
SAT.dropna(axis=0,inplace=True,how='all', subset=['reading', 'math', 'writing'])
print(SAT.loc[:10])

###########################################################
###### sql stuf
###########################################################
conn = sa.create_engine('sqlite:///db/nycedudata.db')

conn.execute('  DROP TABLE IF EXISTS SAT;')
conn.execute('  CREATE TABLE IF NOT EXISTS SAT (\
                test_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                dbn TEXT,\
                school_year INTEGER,\
                test_takers INTEGER,\
                reading INTEGER,\
                math INTEGER,\
                writing NUMERIC,\
                total_rm NUMERIC,\
                FOREIGN KEY (dbn) REFERENCES Schools (dbn)\
                );')

for i in SAT.index:
    values = tuple(SAT.loc[i])
    conn.execute('  INSERT INTO SAT (dbn, school_year, test_takers, reading,\
                        math, writing, total_rm) \
                    VALUES (?,?,?,?,?,?,?);',values)

test = conn.execute('SELECT * FROM SAT LIMIT 5;').fetchall()
print(test)
