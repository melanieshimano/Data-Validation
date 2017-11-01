
# coding: utf-8

# In[1]:

get_ipython().system(' pip install ipywidgets')


# In[2]:

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


# In[3]:

#import excel sheet with work order data
df =pd.read_excel('C:\\Users\\melanie.shimano\\Documents\\Copy15 of FY18 Outcome Budgeting--Data Validation.xlsx', sheetname ='FMD.FY16')


# In[4]:

#index the dataframe
df.set_index("WO_ID",  inplace=True)


# In[5]:

#***SET THE FISCAL YEAR for analysis
FYyear = 2015


# In[6]:

df.head()


# In[7]:

#remove rows where work order duration = open because won't be able to calculate anything from these
#keep only work orders in FY for financial analysis indicated above in FYyear
#keep only PM:CM relevant work orders: HVAC PM, boiler, chiller, HVAC, HVAC Infrastructure, HVAC repair
df =df[df.WO_duration != 'open']
df = df[df.FY == FYyear]


# In[8]:

#drop unneccesary columns in dataframe for ease of view
col_list = ['BLDG#','FY','Month','prob_type']
df = df[col_list]


# In[9]:

#count number of work orders by problem type
df['count'] = df.groupby(['prob_type'])['prob_type'].transform('count')


# In[10]:

#keep only one of each problem type for analysis 
df_prob_type = df.drop_duplicates(subset ='prob_type', keep='last')


# In[11]:

#drop values that are NaN
df_prob_type.dropna()


# In[12]:

#keep only preventative and corrective HVAC related work order problem types
df_pmcm = df_prob_type[df_prob_type['prob_type'].str.contains('HVAC|BOILER|CHILLERS|PREVENTIVE MAINT')==True]


# In[13]:

#create new dataframe of only preventative maintenance to then sum count
df_pm = df_pmcm[df_pmcm['prob_type'].str.contains('PM|PREVENTIVE MAINT')==True]


# In[14]:

#total number of preventative maintenance work orders
PM = df_pm['count'].sum()


# In[15]:

#sum the corrective maintenance tasks
#create new dataframe of only corrective maintenance to then sum count
#need to delete HVAC|PM counts that are included in the "HVAC" selection
df_cm = df_pmcm[(df_pmcm['prob_type'].str.contains('HVAC|BOILER|CHILLERS')==True)&(~df_pmcm['prob_type'].str.contains('PM')==True)]


# In[16]:

#total number of correective maintenance work orders
CM = df_cm['count'].sum()
PMCM = (PM/CM)*100


# In[17]:

print('In Fiscal Year '+ str(FYyear) + ' the ratio of preventative maintenance versus corrective maintenance was ' + str(round (PM/CM,2)) +', or ' + str(round (PMCM,2)) + '%')


# In[ ]:



