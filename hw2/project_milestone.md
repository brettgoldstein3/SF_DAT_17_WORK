# Startup Data Science Projects

## Background
Venture Capital has become increasingly competitive with more traditional financial institutions and angel investors entering the market every year coupled with rapidly decreasing costs to start a company. While this has caused seed and pre-seed rounds to be more and more sought after, they are still have the most risk. The best VCs are experts at picking winners in this risky bunch, but their methods for doing so are often more qualitative than quantitative. The Quant VC movement of recent years has sought to change that.

## Objective
The objective of this project at a high level is to be able to programmatically identify fast growing apps. More specifically, with download and engagement history as metrics, I hope to train a machine learning model to predict the likelihood of an app entering the top 10 on the iOS app store within n weeks.

## Data
App Annie is a data vendor that collects download and rankings data from app stores as well as usage data from apps themselves. 

I will be utilizing the following data points. You can also view an [example data set](../data/appannie-data.csv) from App Annie itself.

| **Data Type** | app_name | week_id  | downloads  | rating_avg_all  | rating_count_all  | release_date_id  | primary_category |
| --- |---| ---| ---| ---| ---|  ---| ---|
| **Example** | Snapchat | 723 | 12390 | 3.2 | 123 | 4598 | Lifestyle | 

Note, ranking has yet to be included in the tables I have access to - working to resolve this now.

## Analysis
Will limit scope to download_country = USA and store = iOS.

## Presentation
Problem statement in VC

Objective and Abstract

App Annie overview

Data points utilized

Execution methodology
* Exported App Annie data from Dreml table available to Google internally
* Included only US downloads/store charts and the iOS apps
* [ what libraries I used ]
* [ how I trained the model ]
* [ how I evaluated results ]

Results
* Technical review of results, statistical significance, etc.
* How confident are we in the model?

Discussion
* What features are most important to tell if an app is going to make it into the top 10? Graph those for top 
* Predictions: Identify a few apps to make it into the top 10 within n weeks. If applicable, discuss accuracy in report.

Next steps
* Further research around why being in the top 10 is significant - suggest data science technique to address this question
* Discuss ways to refine model - what other data points are relevant to add? Why?
* Deeper dive into app categories. Do certain things work better in certain categories? Are some categories easier to predict?

Appendix: Other attempts at this problem
* [Finding Hot Startups with Twitter Data](https://www.cbinsights.com/blog/trending-startups-twitter/?utm_source=CB+Insights+Newsletter&utm_campaign=73677e380e-edit_10_18_2015&utm_medium=email&utm_term=0_9dc0513989-73677e380e-86555729&goal=0_9dc0513989-73677e380e-86555729)
* [Quantitative VC](http://techcrunch.com/2013/06/01/the-quantitative-vc/)
* [Trendify](http://trendify.io/)
