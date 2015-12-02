# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:45:08 2015

@author: brettgoldstein

OBJECTIVE
- utilize various metrics to predict whether or not an app is in the top 10


"""

import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
#import docx
import numpy as np
from sklearn.ensemble import RandomForestClassifier



# define functions

def train_test_rmse(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    linreg = LogisticRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    return np.sqrt(metrics.mean_squared_error(y_test, y_pred))


# Import the dataset
final = pd.read_csv('data/appannie-final.csv')
final.columns
final.shape

# Add a column if its in the top 10
# Looks like there are 1347 instances of an app being in the top 10!
istop10 = [1 if ra <= 10 else 0 for ra in final.ranking]
final['istop10'] = istop10

#check out the columns
final.columns


x = pd.get_dummies(final.primary_category)
final = pd.merge(final,x,left_index=True,right_index=True)
final.istop10.value_counts()
final.primary_category
final.shape

# Comparison Graphs
final[['downloads','ranking']].plot(kind='scatter',x='downloads',y='ranking',logx=True)
final[['rating_avg_all','ranking']].plot(kind='scatter',x='rating_avg_all',y='ranking')
final[['rating_count_cur','ranking']].plot(kind='scatter',x='rating_count_cur',y='ranking')
final[['istop10','downloads']].plot(kind='scatter',x='istop10',y='downloads',logy=True)

# see how the data looks
final['downloads'].value_counts().plot(kind='hist')
final['rating_avg_all'].value_counts().plot(kind='bar')
final['rating_count_cur'].value_counts().plot(kind='bar')
final['ranking'].value_counts().plot(kind='hist')
final['istop10'].value_counts().plot(kind = 'pie')


## FIRST ANALYSIS: predict whether something is in the top 10 or not

# columns we want to test on
#feature_cols = ['downloads','rating_avg_all','rating_count_cur','ranking' ,'istop10']

# select that data from the data frame
cols = ['downloads','rating_count_cur','Photo, Video and Media','istop10']

dataset1 = final[cols]
dataset1.shape

# run a linear regression
X, y = dataset1.drop('istop10', axis = 1), dataset1['istop10']
logreg = LogisticRegression()
logreg.fit(X, y)

print 'intercept: ' + str(logreg.intercept_[0])

sipped1 = zip(cols[:-1], logreg.coef_[0])
for i in sipped1:
	print i
    
train_test_rmse(X, y)



# Random Forest
dataset4 = final.dropna()
dataset4.columns
del dataset4['app_id']
del dataset4['app_name']
del dataset4['primary_category']
del dataset4['rank_category']
del dataset4['appannie_url']

rfclf = RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1)
rfclf.fit(dataset4.drop('istop10', axis = 1), dataset4.istop10)
rfimp = pd.DataFrame({'feature':dataset4.drop('istop10', axis = 1).columns, 'importance':rfclf.feature_importances_})
rfimp.sort(columns='importance',ascending=False)
rfclf.oob_score_

# plot importance!
rfimp.sort(columns='importance',ascending=False).plot(kind='bar',x='feature',y='importance',logy=True)




## SECOND ANALYSIS: predict whether something will be in the top 10 in 3 months
# TAKE THE MAX and AVG to do this easier
# create apps data series
apps = final.app_name.unique()

# Check the average distance between week_ids for each app
# should be 1 if there the week IDs are consecutive

numweeks1 = final.groupby('app_name').week_id.count()
avgweekdelta1 = (final.groupby('app_name').week_id.max() - final.groupby('app_name').week_id.min())/final.groupby('app_name').week_id.count()


# instantiate data frame

#derived = pd.read_csv('data/derived-metrics.csv')


derived = pd.DataFrame()
derived['app_name'] = apps
derived['can_use'] = 0
derived['start_week'] = 0
derived['threemo_week'] = 0
derived['sixmo_week'] = 0
derived['istop10'] = 0

derived['avg_downloads'] = 0
#derived['sixmo_downloads'] = 0
#derived['threemo_downloads'] = 0
derived['corcoef_downloads'] = 0

derived['avg_rank'] = 0
#derived['sixmo_rank'] = 0
#derived['threemo_rank'] = 0
derived['corcoef_rank'] = 0

derived['category'] = ''



for app in apps:
	
	# skip ones that don't have enough weeks or have non-consecutive weeks - this is a killer filter
	# gets us down to 388 non top 10 apps and 13 top 10 apps
	# maybe dont worry about consecutive weeks? or just use months?
	loc = derived[derived.app_name == app].index[0]
	
	cat = final[final.app_name == app].primary_category.head(1).values[0]
	derived.category[loc] = cat
	
	if numweeks1[app] < 36 or avgweekdelta1[app] >= 2:
		derived.can_use[loc] = 0
		continue
	else:
		derived.can_use[loc] = 1
		if final[final.app_name == app].istop10.sum() == 0:
			startweek = final[final.app_name == app].week_id.max()
			
		# for apps that were in the top 10, start with the most recent top spot    
		else:
			startweek = final[(final.app_name == app) & (final.istop10 == 1)].week_id.max()
			derived.istop10[loc] = 1
		
		if app in final[final.istop10 == 1]:
			derived.istop10[loc] = 1
		
		# get the time bounds by week ID
		threemo = startweek - 12
		sixmo = startweek - 24

		# record the weeks
		derived.start_week[loc] = float(startweek)
		derived.threemo_week[loc] = float(threemo)
		derived.sixmo_week[loc] = float(sixmo)

		# get the correlation coefficients for rank and downloads over time period
		co = final[(final.app_name == app) & (final.week_id <= threemo) & (final.week_id >= sixmo)][['downloads','ranking','week_id']].corr()
		doco = co['downloads'].week_id
		raco = co['ranking'].week_id
		
		derived.corcoef_downloads[loc] = float(doco)
		derived.corcoef_rank[loc] = float(raco)

		# record average downloads over time period		
		downs = final[(final.app_name == app) & (final.week_id <= threemo) & (final.week_id >= sixmo)].downloads.mean()		
		derived.avg_downloads[loc] = float(downs)
		
		# record average rank over time period
		ranks = final[(final.app_name == app) & (final.week_id <= threemo) & (final.week_id >= sixmo)].ranking.mean()		
		derived.avg_rank[loc] = float(ranks)
		
		#threemo_dl = final[(final.app_name == app) & (final.week_id == threemo)].downloads
		#sixmo_dl = final[(final.app_name == app) & (final.week_id == sixmo)].downloads
		
		#derived.sixmo_downloads[loc] = float(threemo_dl)
		#derived.threemo_downloads[loc] = float(sixmo_dl)		
		
		#derived.sixmo_rank[loc] = float(threemo_ra)
		#derived.threemo_rank[loc] = float(sixmo_ra)
		
		#X = final[(final.app_name == app) & (final.week_id <= threemo) & (final.week_id >= sixmo)].week_id
		#y = final[(final.app_name == app) & (final.week_id <= threemo) & (final.week_id >= sixmo)][['downloads','ranking']]
		#linreg = LinearRegression()
		#linreg.fit(X, y)
		#downs_int = linreg.intercept_
		#downs_coef = linreg.coef_
		#print downs_coef
		
		#rmse = train_test_rmse(X, y)
		#rmse


derived[derived.app_name == 'Snapchat']
derived.to_csv('derived-metrics.csv')

derived_clean = derived[derived.can_use == 1]
derived_clean.dropna() # not working?

# add in dummy columns for category
x = pd.get_dummies(derived_clean.category)
derived_clean = pd.merge(derived_clean,x,left_index=True,right_index=True)

# total number of positive and negative values
derived_clean.istop10.value_counts()
derived_clean.columns
derived[cols].dropna()

# Logistic Regression
all_cols = derived_clean.columns[2:]
cols = ['avg_downloads','corcoef_downloads','istop10']

dataset2 = derived_clean[cols].dropna()
del dataset2['category']
dataset2.columns

X, y = dataset2.drop('istop10', axis = 1), dataset2['istop10']
logreg = LogisticRegression()
logreg.fit(X, y)

print 'intercept: ' + str(logreg.intercept_[0])
print logreg.coef_[0]

sipped = zip(cols, logreg.coef_[0])
for i in sipped:
	print i
    
train_test_rmse(X, y)

ri_pred = logreg.predict(X)
#plt.plot(dataset2.avg_rank, ri_pred, color='red')


# Random Forest
dataset3 = derived_clean.dropna()
del dataset3['app_name']
del dataset3['can_use']
del dataset3['category']

rfclf = RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1)
rfclf.fit(dataset3.drop('istop10', axis = 1), dataset3.istop10)
rfimp = pd.DataFrame({'feature':dataset3.drop('istop10', axis = 1).columns, 'importance':rfclf.feature_importances_})
rfimp.sort(columns='importance',ascending=False)
rfclf.oob_score_

# plot importance!
rfimp.sort(columns='importance',ascending=False).plot(kind='bar',x='feature',y='importance')

