#!/usr/bin/env python
# coding: utf-8

# TASK III

# In[1]:


import pandas as pd


# In[2]:


df_2014 = pd.read_csv('Analytics_mindset_case_studies_PCard_FY2014.csv', parse_dates=['Transaction Date', 'Posted Date'], encoding='ISO-8859-1', header = 0)


# In[3]:


df_2014.dtypes


# In[4]:


start_date = '2014-01-01'
end_date = '2014-12-31'
OSU2014 = ((df_2014['Transaction Date'] >= start_date) & (df_2014['Transaction Date'] <= end_date))
df_2014 = df_2014[OSU2014]
onlyOSU = df_2014['Agency Name'] == 'OKLAHOMA STATE UNIVERSITY'
df_2014 = df_2014[onlyOSU]
df_2014


# In[5]:


df_2015 = pd.read_csv('Analytics_mindset_case_studies_PCard_FY2015.csv', parse_dates=['Transaction Date', 'Posted Date'], encoding='ISO-8859-1', header = 0)
df_2015['Amount'] = df_2015['Amount'].str.replace('$','').str.replace(',','').str.replace('(','-').str.replace(')','')
df_2015['Amount'] = df_2015['Amount'].astype(float)


# In[6]:


df_2015.dtypes


# In[7]:


df_2015


# In[8]:


##There's no transactions of 2015 in this data, only 2014
onlyOSU2015 = df_2015['Agency Name'] == 'OKLAHOMA STATE UNIVERSITY'
onlyOSU2015
df_2015 = df_2015[onlyOSU2015]
df_2015


# In[9]:


mynames = ["Agency_Number", "Agency_Name", "Cardholder_LastName", "Cardholder_FirstInitial", "Descr", "Amount", "Vendor", "TransactionDate", "PostedDate", "MCC"]


# In[10]:


filename = pd.concat([df_2014, df_2015], names = mynames)


# In[11]:


##We assuume that we have to drop the transactions with NaT under Transaction Date as there is no way of knowing it's date 
##Not doing so will incorrectly inflate our figures. More information on them is required
filename = filename[filename['Transaction Date'].notnull()]
filename


# In[12]:


filename['Transaction Date'] = filename['Transaction Date'].dt.strftime('%m/%d/%Y')


# In[13]:


filename['Posted Date'] = filename['Posted Date'].dt.strftime('%m/%d/%Y')


# In[14]:


filename


# In[ ]:





# In[15]:


filename.shape


# Data set has 116,031 rows!

# In[16]:


filename['Amount'].sum()


# In[17]:


df_2014['Amount'].sum()


# In[18]:


df_2015['Amount'].sum()


# In[ ]:





# TASK V

# Cleaning the date: 

# In[19]:


PCard = filename.copy()


# In[20]:


PCard.describe


# In[21]:


Card_Name = PCard['Cardholder First Initial'] + ' ' + PCard['Cardholder Last Name']


# In[22]:


PCard['Cardholder_name'] = Card_Name


# In[23]:


PCard = PCard.drop(['Cardholder Last Name', 'Cardholder First Initial'], axis=1)


# In[24]:


PCard.head()


# 1. User shall not spend more than $5,000 per transaction:

# In[25]:


Question1 = PCard[['Amount', 'Cardholder_name', 'Description', 'Vendor', 'Transaction Date', 'Posted Date']]
morethan5k = Question1['Amount'] > 5000
Question1 = Question1[morethan5k].sort_values('Amount', ascending = False)
Question1


# 2. User shall not spend more than $50,000:

# In[26]:


Question2 = PCard[['Cardholder_name', 'Amount']]
Total_amount = Question2.groupby('Cardholder_name').sum()
over50k = Total_amount['Amount'] >= 50000
Total_amount[over50k].sort_values(['Amount'], ascending=False)


# 3. User shall not spend more than $10,000 per month without approval

# In[40]:


Question3 = PCard.copy()
Question3 = Question3[['Transaction Date', 'Cardholder_name', 'Amount']]
Question3 = Question3.set_index(['Transaction Date'])
Question3.index = Question3.index.strftime('%B')
Question3.index.name = 'Transaction Date'
by_month = Question3.groupby(['Transaction Date','Cardholder_name']).sum()
noMore10k = by_month['Amount'] > 10000
by_month[noMore10k].sort_values('Transaction Date')


# 4. People who split more than $5,000 between two or more swipes

# In[28]:


Question4 = PCard.copy()
Question4 = Question4[['Vendor', 'Merchant Category Code (MCC)', 'Cardholder_name', 'Transaction Date', 'Amount']]
Question4 = Question4.groupby(['Vendor', 'Cardholder_name', 'Transaction Date']).agg({'Amount': 'sum', 'Merchant Category Code (MCC)': 'count'}).reset_index().rename(columns={'Merchant Category Code (MCC)': 'NumberSwipes'})
morethan1and5k = ((Question4.NumberSwipes > 1) & (Question4.Amount > 5000))
Question4 = Question4[morethan1and5k].sort_values('Transaction Date')
Question4


# Question 5 

# In[29]:


Question5 = Question4.groupby('Cardholder_name').count()
Question5

