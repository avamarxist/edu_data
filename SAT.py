# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 21:45:27 2017

@author: bahar
"""
import pandas as pd
import re

SAT = pd.read_json("https://data.cityofnewyork.us/resource/734v-jeq5.json")


math = SAT['sat_math_avg_score']
english=SAT['sat_critical_reading_avg_score']
writing=SAT['sat_writing_avg_score']

math = math.apply(pd.to_numeric,args=('coerce',))
english = english.apply(pd.to_numeric,args=('coerce',))
writing = writing.apply(pd.to_numeric,args=('coerce',))

SAT['sat_math_avg_score'] = math
SAT['sat_critical_reading_avg_score'] = english
SAT['sat_writing_avg_score'] = writing

#print("Test: len(math) = " + str(len(math)) + ' len(SAT[math])) = ' + str(len(SAT['sat_math_avg_score'])))

total_1600=[]
for i in range(len(math)):
    if math[i] != None and english[i] != None:
        total = math[i] + english[i]
        total_1600.append(total)
#print(total_1600)
SAT['Total_1600'] = total_1600

district=[]
borough = []
school_num = []
for i in range(len(math)):
    if SAT['dbn'][i] != None:
            dist_search = re.compile('^\d\d')
            dist = dist_search.search(SAT['dbn'][i])
            district.append(SAT['dbn'][i][dist.start():dist.end()])

            boro_search = re.compile('(?<=\d\d)[A-Z]+')
            boro = boro_search.search(SAT['dbn'][i])
            borough.append(SAT['dbn'][i][boro.start():boro.end()])

            school_search = re.compile('(?<=[A-Z])\d+')
            school = school_search.search(SAT['dbn'][i])
            school_num.append(SAT['dbn'][i][school.start():school.end()])

SAT['District'] = district
SAT['Boro'] = borough
SAT['School_Num'] = school_num


#print(top)
#print('Top ' + str(topn) + " overlap: " + str(len(top)))

#print(math)

LCGMS = pd.read_excel('res/LCGMS_SchoolData_additional_geocoded_fields_added_.xlsx')
zipdata = pd.read_excel('res/MedianZIP-2006-2010.xlsx')
#print(LCGMS.head())
#geo_data_raw = LCGMS[['ATS System Code','NTA_Name','Latitude','Longitude']]

lat = []
long = []
hood = []
zipcode = []
for dbn in SAT['dbn']:
    geo_row = LCGMS.loc[LCGMS['ATS System Code'] == dbn]
    geo_row_index = geo_row.index
    if geo_row_index.isnull() == False:
        geo_row_index = geo_row_index[0]
        lat_temp = float(LCGMS['Latitude'][geo_row_index])
        if lat_temp == None:
            lat_temp = '-'
        lat.append(lat_temp)
        long_temp = float(LCGMS['Longitude'][geo_row_index])
        if long_temp == None:
            long_temp = '-'
        long.append(long_temp)
        hood_temp = str(LCGMS['NTA_Name'][geo_row_index])
        if hood_temp == 'nan':
            hood_temp = '-'
        hood.append(hood_temp)
        zip_temp = int(LCGMS['Zip'][geo_row_index])
        if zip_temp == None:
            zip_temp = '-'
        zipcode.append(zip_temp)
    else:
        lat.append('-')
        long.append('-')
        hood.append('-')
        zipcode.append('-')
SAT['Latitude'] = lat
SAT['Longitude'] = long
SAT['Nhood'] = hood
SAT['Zip'] = zipcode

income = []
for z in SAT['Zip']:
    if z != '-':
        zip_row = zipdata.loc[zipdata['Zip']==z].index
        if zip_row.isnull() == False:
            income_row = zip_row[0]
            income_temp = int(zipdata['Median'][zip_row])
            if income_temp == None:
                income_temp = '-'
            income.append(income_temp)
        else:
            income.append('-')
    else:
        income.append('-')
SAT['Med Income'] = income

#Check the columns in the main for loop if you change this
sat_columns = ['sat_critical_reading_avg_score','sat_math_avg_score','sat_writing_avg_score',
               'Total_1600','num_of_sat_test_takers','dbn','Boro','District','School_Num','school_name',
               'Zip','Nhood','Med Income','Latitude','Longitude']
SAT = SAT[sat_columns]

SAT.to_csv('res/SAT_dataframe.csv')
