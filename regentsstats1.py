import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import sqlalchemy as sa



engine = sa.create_engine('sqlite:///db/nycedudata.db')
regents_df = pd.read_sql_table('Regents',engine)

num_cols = ['mean_score', 'num_lt_65', 'pct_lt_65','num_gt_65', 'pct_gt_65',
            'num_gt_80', 'pct_gt_80']

regents_df = regents_df.applymap( lambda x: None if x == 's' else x )
regents_df = regents_df.applymap( lambda x: float(x) if type(x)==int else x)
regents_df.drop('test_id',1)

"""
create tables of stats
"""

for col in num_cols:
    regents_df[col] = regents_df[col].apply( lambda x: float(x) )

means = [ np.mean(regents_df[col].astype(float)) for col in num_cols ]
regents_stats = pd.DataFrame(means, index = num_cols, columns = ['col_mean'])

regents_stats['stdev'] = [ np.std(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['col_median']= [ np.median(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['iqr'] = [ st.iqr(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['five_num'] = [ np.percentile(regents_df[col].astype(float),[0, 25, 50, 75, 100]) for col in num_cols ]
regents_stats['deciles'] = [ np.percentile(regents_df[col].astype(float),[10,20,30,40,50,60,70,80,90]) for col in num_cols ]

print(regents_stats['col_median'])
algebra_scores = regents_df[regents_df['exam_name'] == 'common core algebra']
means = [ np.mean(algebra_scores[col].astype(float)) for col in num_cols ]
alg_stats = pd.DataFrame(means, index = num_cols, columns = ['col_mean'])

alg_stats['stdev'] = [ np.std(algebra_scores[col].astype(float)) for col in num_cols ]
alg_stats['col_median']= [ np.median(algebra_scores[col].astype(float)) for col in num_cols ]
alg_stats['iqr'] = [ st.iqr(algebra_scores[col].astype(float)) for col in num_cols ]
alg_stats['five_num'] = [ np.percentile(algebra_scores[col].astype(float),[0, 25, 50, 75, 100]) for col in num_cols ]
alg_stats['deciles'] = [ np.percentile(algebra_scores[col].astype(float),[10,20,30,40,50,60,70,80,90]) for col in num_cols ]
alg_stats = st.describe(algebra_scores['mean_score'].astype(float))

"""
plot boxplots broken down by subgroups
"""

# by_exam = {}
# stat = 'Percent Scoring Below 65'
# category = 'Demographic Variable'
# for exam in set(regents_df[category]):
#     by_exam[exam] = list(regents_df[regents_df[category] == exam][stat])
# # regents_by_exam = pd.DataFrame(by_exam)
# plt.boxplot(by_exam.values(), labels = by_exam.keys())
# plt.plot([0, len(by_exam.keys())+0.5],[regents_stats['col_median'][stat], regents_stats['col_median'][stat]])
# plt.title(category + " - " + stat)
# plt.xticks(rotation = 90)
# plt.show()

"""
plot histograms broken down by subgroups
"""

# by_exam = {}
# for stat in num_cols:
#     for category in ['demographic_variable','regents_exam']:
#         for cat in set(regents_df[category]):
#             by_exam = list(regents_df[regents_df[category] == cat][stat])
#             fig = plt.figure()
#             hist = plt.hist(by_exam, color = 'powderblue', edgecolor = 'black')
#             mode_freq = np.max(list(hist[0]))
#             plt.plot([np.mean(by_exam), np.mean(by_exam)], [0, np.max(hist[0])], color = 'darkorange', linewidth = 3.0)
#             plt.plot([np.median(by_exam), np.median(by_exam)], [0, np.max(hist[0])], color = 'darkorchid', linewidth = 3.0)
#             plt.xlabel(stat)
#             plt.title(category + " - " + cat)
#             cat = cat.replace(" ","_")
#             cat = cat.replace("/","_")
#             #fig.savefig('out/hist_'+category+"--"+cat +"--"+stat+".png")
#             plt.close()
#plt.show()
# plt.scatter(regents_df['mean_score'],regents_df['percent_scoring_65_or_above'])
