# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:30:54 2018

@author: bahar
"""

import pandas as pd
import nummpy
import sqlalchemy as sa

LCGMS = pd.read_excel('res/LCGMS_SchoolData_additional_geocoded_fields_added_.xlsx')
# print(LCGMS.head())
#print(LCGMS.columns)
#

LCGMS.columns = [str(col).lower() for col in LCGMS.columns]
geo_data_raw = LCGMS[['ats system code','building code', 'location name', 'managed by name',
                        'city', 'zip', 'nta', 'nta_name', 'community district', 'council district',
                        'latitude','longitude']]
geo_data_raw.columns = ['dbn','building code', 'school name', 'managed by',
                        'city', 'zip', 'nta', 'neighborhood', 'community district', 'council district',
                        'latitude','longitude']


geo_data_raw = geo_data_raw.applymap(lambda x: x.lower() if type(x) == str else x)


#print(geo_data_raw.size)

geo_data = geo_data_raw.dropna(subset= ['dbn'])
#print(geo_data.size)

print(geo_data.loc[geo_data['dbn'] == '01m015'])
print(geo_data.loc[48])

dupes = geo_data.duplicated(subset='dbn',keep='first')
print('Duplicate count: {}'.format(str(list(dupes).count(True))))

conn = sa.create_engine('sqlite:///db/nycedudata.db')

for i in geo_data.index:
    vals = [str(x) for x in geo_data.loc[i]]
    values = tuple(vals)
    conn.execute('INSERT INTO Schools VALUES (?,?,?,?,?,?,?,?,?,?,?,?);',values)


test = conn.execute('SELECT * FROM Schools LIMIT 5;').fetchall()
print(test)
