"""
Statistical analyses of demographic data from nycedudata database
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import sqlalchemy as sql
import matplotlib.pyplot as plt

engine = sql.create_engine('sqlite:///db/nycedudata.db')

query1 = "SELECT * FROM Schools;"
schools_df = pd.read_sql_query(query1,engine)

query_string = "SELECT Regents.test_id, Demographics.demo_id, Regents.dbn, Regents.year, Regents.exam_name, \
Regents.demo_var AS test_demo, Demographics.demo_var as school_demo, \
Regents.mean_score, Regents.pct_lt_65, Regents.pct_gt_65, Regents.pct_gt_80, \
Demographics.total_enrollment, Regents.test_num, \
Demographics.demo_num as school_demo_num, Demographics.demo_pct AS school_demo_pct \
FROM Regents JOIN Demographics USING (dbn, year) \
WHERE Regents.demo_var = 'all students' AND Demographics.demo_var = 'white';"

demo_df = pd.read_sql_query(query_string, engine)


###################################################################################################
###################################################################################################

plt.scatter(demo_df['school_demo_pct'],demo_df['pct_gt_80'])
plt.xlabel('school_demo_pct')
plt.ylabel('pct_gt_80')
plt.show()
