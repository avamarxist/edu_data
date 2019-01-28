import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt



regents_df = pd.read_csv('res/regents_cleaner.csv', na_values = 's')
#print(regents_df.head())
#print(len(regents_df))

col_names = [col.lower().replace(" ","_") for col in regents_df.columns]
regents_df.columns = col_names

num_cols = ['mean_score',
    'number_scoring_below_65', 'percent_scoring_below_65',
    'number_scoring_65_or_above', 'percent_scoring_65_or_above',
    'number_scoring_80_or_above', 'percent_scoring_80_or_above']

regents_df.dropna(axis=0, how = 'all', inplace = True,subset = num_cols)
regents_df.dropna(axis=0,inplace = True, subset = ['regents_exam'])

# regents_df = regents_df.applymap( lambda x: str(x).replace("/", "_"))
# print(set(regents_df['regents_exam']))
# print(type(regents_df['regents_exam'][32]))
#print(regents_df.head())
#print(len(regents_df))

#print(set(regents_df['Regents Exam']))

for col in num_cols:
    regents_df[col] = regents_df[col].apply( lambda x: float(x) )

means = [ np.mean(regents_df[col].astype(float)) for col in num_cols ]
regents_stats = pd.DataFrame(means, index = num_cols, columns = ['col_mean'])

regents_stats['stdev'] = [ np.std(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['col_median']= [ np.median(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['iqr'] = [ st.iqr(regents_df[col].astype(float)) for col in num_cols ]
regents_stats['five_num'] = [ np.percentile(regents_df[col].astype(float),[0, 25, 50, 75, 100]) for col in num_cols ]
regents_stats['deciles'] = [ np.percentile(regents_df[col].astype(float),[10,20,30,40,50,60,70,80,90]) for col in num_cols ]

# algebra_scores = regents_df[regents_df['Regents Exam'] == 'common core algebra']
# means = [ np.mean(algebra_scores[col].astype(float)) for col in num_cols ]
# alg_stats = pd.DataFrame(means, index = num_cols, columns = ['col_mean'])
#
# alg_stats['stdev'] = [ np.std(algebra_scores[col].astype(float)) for col in num_cols ]
# alg_stats['col_median']= [ np.median(algebra_scores[col].astype(float)) for col in num_cols ]
# alg_stats['iqr'] = [ st.iqr(algebra_scores[col].astype(float)) for col in num_cols ]
# alg_stats['five_num'] = [ np.percentile(algebra_scores[col].astype(float),[0, 25, 50, 75, 100]) for col in num_cols ]
# alg_stats['deciles'] = [ np.percentile(algebra_scores[col].astype(float),[10,20,30,40,50,60,70,80,90]) for col in num_cols ]
#alg_stats = st.describe(algebra_scores['Mean Score'].astype(float))


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

# by_exam = {}
# for stat in num_cols:
#     for category in ['demographic_variable','regents_exam']:
#         for cat in set(regents_df[category]):
#             by_exam = list(regents_df[regents_df[category] == cat][stat])
#             fig = plt.figure()
#             plt.hist(by_exam, edgecolor = 'black')
#             #plt.plot([0, len(by_exam.keys())+0.5],[regents_stats['col_median'][stat], regents_stats['col_median'][stat]])
#             plt.xlabel(stat)
#             plt.title(category + " - " + cat)
#             cat = cat.replace(" ","_")
#             cat = cat.replace("/","_")
#             #fig.savefig('out/hist_'+category+"--"+cat +"--"+stat+".png")
#             plt.close()
# #plt.show()
plt.scatter(regents_df['mean_score'],regents_df['percent_scoring_65_or_above'])
