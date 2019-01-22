# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:30:54 2018

@author: bahar
"""

import pandas as pd

LCGMS = pd.read_excel('Ed Data\LCGMS_SchoolData_additional_geocoded_fields_added_.xlsx')
print(LCGMS.head())
geo_data_raw = LCGMS[['Administrative District Code','Building Code','NTA_Name','Latitude','Longitude']]
