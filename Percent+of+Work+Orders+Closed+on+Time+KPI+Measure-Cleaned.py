
# coding: utf-8

# In[1]:

get_ipython().system(' pip install ipywidgets')


# In[2]:

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import *
get_ipython().magic('matplotlib inline')


# In[3]:

#import excel sheet with work order data
df =pd.read_excel('C:\\Users\\melanie.shimano\\Documents\\Copy15 of FY18 Outcome Budgeting--Data Validation.xlsx', sheetname ='FMD.FY16')


# In[4]:

#index the dataframe
df.set_index("WO_ID",  inplace=True)


# In[5]:

#***SET THE FISCAL YEAR for analysis
FYyear = 2016


# In[6]:

df.head()


# In[7]:

#remove rows where work order duration = open because won't be able to calculate anything from these
#keep only work orders in FY for financial analysis indicated above in FYyear
df =df[df.WO_duration != 'open']
df = df[df.FY == FYyear]


# In[8]:

#add count of each prob_type to the data index
df['Counts']=df.groupby(['prob_type'])['WO_duration'].transform('count')


# In[9]:

#drop unneccesary columns in dataframe for ease of view
col_list = ['BLDG#','FY','Month','prob_type', 'WO_duration', 'Counts']
df = df[col_list]


# In[10]:

df['total_duration']= df.groupby(['prob_type'])['WO_duration'].transform('sum')


# In[11]:

#calculate average work order duration per problem type (=counts/total_duration) and add value in new column
df['avg_total_duration']=df['total_duration']/df['Counts']


# In[12]:

#check to see if individual work order closed at or equal to the average work order duration for that problem type
#add new column "KPI_met" fill with "yes" if WO_duration <= avg_total_duration, otherwise fill 'no'
df['closed_on_time']= np.where(df['WO_duration']<=df['avg_total_duration'], 'yes','no')


# In[13]:

#create new df of only KPIs that are met
df_yes = df[df.closed_on_time == 'yes']


# In[14]:

#count number of KPI met per problem type
df_count = df_yes.groupby('prob_type')['closed_on_time'].count()


# In[15]:

#turn series into a df to later merge with original dataframe and keep WO_ID
df_KPI = pd.DataFrame({'prob_type': df_count.index, 'on_time_count':df_count.values})


# In[16]:

#new df (by merge) with number of KPI met in new column
df_wo = df.assign(on_time_count =df['prob_type'].map(df_KPI.set_index('prob_type')['on_time_count']))


# In[17]:

#new df (by merge) with number of KPI met in new column
df_wo = df.assign(on_time_count =df['prob_type'].map(df_KPI.set_index('prob_type')['on_time_count']))


# In[18]:

#calculate percentage of Work Orders that meet KPI and store in new column 'percent_KPI_met'
df_wo['percent_KPI_met']=(df_wo['on_time_count']/df_wo['Counts'])*100


# In[19]:

#create dataframe of only unique problem types for high level analysis of KPIs met
df_wo_final = df_wo.drop_duplicates(subset = 'prob_type', keep ='last')
df_wo_final


# In[20]:

#get total values to calculate total number of KPI met
WO_total_count = df_wo_final['Counts'].sum()

WO_KPI_met_count = df_wo_final['on_time_count'].sum()

percent_KPI_met = (WO_KPI_met_count/WO_total_count)*100


# In[21]:

#print total percentage of KPI met and total number of KPI met for the year
print('Percent of Work Orders closed on time in FY '+ str(FYyear) +' = ' + str(round (percent_KPI_met, 2)) + "%, which means " +
      str(round(WO_KPI_met_count,0)) + ' out of ' + str(round (WO_total_count,2)) + ' work orders were closed on time')


# In[22]:

#sort work order problem types by the percentage that did not meet the KPI (i.e. the percent that weren't closed on time)
df_wo_final['not_on_time']=df_wo_final['Counts'] -df_wo_final['on_time_count']
df_wo_final['percent_KPI_not_met']= (df_wo_final['not_on_time']/df_wo_final['Counts'])*100
df_wo_final = df_wo_final.sort_values('percent_KPI_not_met')
#graph the top 20 percent work orders by problem type that were not closed on time
df_wo_final[50:].plot(x='prob_type', y='percent_KPI_not_met', kind='barh', title= 'Percent of Work Orders Not Closed on Time by Problem Type', figsize=(20,20))


# In[ ]:



