# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 20:07:33 2018

@author: bahar
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

SAT = pd.read_csv('res/SAT_dataframe.csv',index_col=0)
"""
Run descriptive statistics
"""
#print(SAT.columns)

for col in SAT.columns[0:4]:
    col = str(col)
    col_max = SAT[col].idxmax()
    col_min = SAT[col].idxmin()
    col_max_id = SAT['dbn'][col_max]
    col_min_id = SAT['dbn'][col_min]
    col_max_name = SAT['school_name'][col_max]
    col_min_name = SAT['school_name'][col_min]
    col_max_score = SAT[col][col_max]
    col_min_score = SAT[col][col_min]
    print("Max " + col + ': ' + str(col_max_id)+ ' ' + str(col_max_name) + ', ' + str(col_max_score ))
    print("Min " + col + ': ' + str(col_min_id)+ ' ' + str(col_min_name) + ', ' + str(col_min_score ))

    col_score = SAT[col].dropna()
    col_mean = np.mean(col_score)
    print("Mean " + col + ': '+ str(col_mean))
    col_med = np.median(col_score)
    print("Median " + col + ': '+ str(col_med))

    print("")

    if col_max_score <=800:
        scrange=[200,800]
    elif col_max_score > 1600:
        scrange=[600,2400]
    else:
        scrange=[400,1600]

    quartiles = np.percentile(col_score,[25,75])
    iqr = quartiles[1]-quartiles[0]
    deciles = np.percentile(col_score,[10,20,30,40,50,60,70,80,90, 95, 99])

    chart=plt.figure(figsize=[16,6])

    chart.add_subplot(1,2,1)
    histdata=plt.hist(col_score, edgecolor='black')
    ymax=max(histdata[0])
    plt.plot([col_med,col_med],[0,ymax],color='red',lw=5)
    plt. plot([col_mean,col_mean],[0,ymax],color='green',lw=5)
#    plt. plot([col_min_score,col_min_score],[0,ymax],color='black',lw=5)
#    plt. plot([col_max_score,col_max_score],[0,ymax],color='black',lw=5)
    plt. plot([quartiles[0],quartiles[0]],[0,ymax],color='black',lw=5)
    plt. plot([quartiles[1],quartiles[1]],[0,ymax],color='black',lw=5)
    for dec in deciles:
        plt.plot([dec,dec],[0,25],color='black',lw=2)
    plt.xlim(scrange)
    medtext= "Median = %f" % col_med
    meantext = "Mean = %f" % col_mean
    plt.text(1.2*col_mean,0.8*ymax,medtext,color='red')
    plt.text(1.2*col_mean,0.7*ymax,meantext,color='green')
    plt.title(col)


    iqrtext = "IQR = %i" % int(iqr)
    mintext = "Min - %i |" % int(col_min_score)
    Q1text = "Q1 - %i |" % int(quartiles[0])
    medtext = "Med | %i" % int(col_med)
    Q3text = "| Q3 - %i" % int(quartiles[1])
    maxtext = "| Max - %i" % int(col_max_score)

    chart.add_subplot(1,2,2)
    plt.boxplot(col_score, vert=False)
    plt.xlim(scrange)
    plt.title(col)
    plt.text(col_min_score,1.1,mintext,color='black',horizontalalignment='right')
    plt.text(quartiles[0],0.87,Q1text,color='black',horizontalalignment='right')
    plt.text(col_med,1.1,medtext,color='red',horizontalalignment='center')
    plt.text(quartiles[1],0.87,Q3text,color='black',horizontalalignment='left')
    plt.text(col_max_score,1.1,maxtext,color='black',horizontalalignment='left')
    plt.text(col_med,0.8,iqrtext,color='blue',horizontalalignment='center')
    for dec in deciles:
        plt.plot([dec,dec],[0.975,1.025],'b--', color='black',lw=1)


total_1600_sort = SAT['Total_1600'].dropna()
total_1600_sort = sorted(total_1600_sort)
total_1600_gaps = []
for i in range(1,len(total_1600_sort)):
    gap = total_1600_sort[i] - total_1600_sort[i-1]
    if pd.isna(gap):
        gap = total_1600_sort[i] - total_1600_sort[i-2]
    total_1600_gaps.append(gap)

chart = plt.figure(figsize=[16,6])
chart.add_subplot(1,2,1)
total_1600_sort.pop(0)
plt.scatter(range(len(total_1600_sort)), total_1600_gaps)

rank_corrected = [i - len(total_1600_sort)/2 for i in range(len(total_1600_sort))]

chart.add_subplot(1,2,2)
#plt.scatter(rank_corrected, total_1600_sort)
polydeg = 7
score_poly_fit = np.polyfit(rank_corrected, total_1600_sort, deg=polydeg)
#rank_float = [float(i) for i in range(len(total_1600_sort))]
#score_poly = [score_poly_fit*[1,x,x^2] for x in rank_float]
score_poly = []
for x in rank_corrected:
    y=0
    for i in range(polydeg+1):
        y += score_poly_fit[i]*x**(polydeg-i)
    score_poly.append(y)
plt.scatter(rank_corrected,total_1600_sort)
plt.scatter(rank_corrected,score_poly)
#print(score_poly_fit)

hood_ar = np.array(SAT['Nhood'])
for i in range(hood_ar.size):
    if type(hood_ar[i]) != str:
        print(str(i) + " in hood_ar is type " + str(type(hood_ar[i])))

hood_list, hood_counts = np.unique(hood_ar,return_counts=True,axis=None)
#print(hood_list.head())
#print(hood_counts.head())

hood_df = pd.DataFrame(data=hood_list,columns=['Neighborhood'])
hood_df['Frequency'] = hood_counts
hood_math_avg = []
for hood in hood_list:
    temp = SAT.loc[SAT['Nhood'] == hood]
    hood_mean = np.mean(temp['sat_math_avg_score'])
    hood_math_avg.append(hood_mean)
hood_df['Math Avg'] = hood_math_avg
hood_df = hood_df.sort_values('Math Avg', ascending=False)
chart = plt.figure(figsize = [16,6])
plt.bar(hood_df['Neighborhood'],hood_df['Math Avg'])
plt.xticks(rotation=90)
hood_df.sort_values('Math Avg')
#print(hood_df.head())

SAT_copy = SAT.dropna(axis=0,how='any',subset=['Total_1600','Med Income'])
SAT_copy = SAT_copy[SAT['Med Income'] != '-']
SAT_copy['Med Income'] = [int(m) for m in SAT_copy['Med Income']]
SAT_copy = SAT_copy.sort_values(by='Med Income')
income = SAT_copy['Med Income']
income_ar = np.array(income)
total_1600_corrected = SAT_copy['Total_1600']
total_ar = np.array(total_1600_corrected)
A = np.vstack([income_ar, np.ones(len(income_ar))]).T
chart = plt.figure(figsize=[16,6])
plt.scatter(income,total_1600_corrected)
slope, intercept, r_value, p_value, std_err = stats.linregress(income_ar, total_ar)
plt.plot(income_ar,slope*income_ar+intercept)
plt.text(80000,1200,s='m = ' + str(slope))
plt.text(80000,1150,s='c = ' + str(intercept))
plt.text(80000,1250,s='r = ' + str(r_value))
