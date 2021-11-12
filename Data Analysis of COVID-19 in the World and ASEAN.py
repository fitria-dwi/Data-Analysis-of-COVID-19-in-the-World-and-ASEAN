#!/usr/bin/env python
# coding: utf-8

# **Author: Fitria Dwi Wulandari (wulan391@sci.ui.ac.id) - September 9, 2021.**

# # Data Analysis of COVID-19 in the World and ASEAN

# ### Data Loading

# In[1]:


# Import libraries
import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)


# In[2]:


# Import dataset
covid19_url = "https://dqlab.id/data/covid19_worldwide_2020.json"
covid19 = pd.read_json(covid19_url)

print("Dataset size: %d columns dan %d rows.\n" % covid19.shape)
print("Top 5 data:\n",covid19.head(5))


# ### Reformat Data Frame

# In[3]:


print("Information of initial data frame :")
covid19.info()


# `date` column already of type numpy.datetime64[ns], then this column can be set as index for **covid19** data frame.

# In[4]:


covid19 = covid19.set_index("date").sort_index()

print("\nInformation of data frame after reformatting:")
covid19.info()


# ### Handling Missing Values

# Next, we will eliminate rows from data that are detected have missing values.

# In[5]:


print("The number of Missing Values for each columns:")
print(covid19.isna().sum())

covid19.dropna(inplace=True)

print("\nThe number of Missing Values for each columns after imputation:")
print(covid19.isna().sum())


# ### Countries Data Loading

# In[6]:


countries_url = "https://dqlab.id/data/country_details.json"
countries = pd.read_json(countries_url)
print(countries.head())


# ### Merge Covid19 Data dan Countries Data

# In[7]:


covid_merge = pd.merge(covid19.reset_index(), countries, on="geo_id").set_index("date")
print(covid_merge.head())


# Note: **covid19** data frame has an index on the `date` column, so it needs .reset_index()). After the merge, the index can be set back to the `date` column.

# ### Calculating Fatality Ratio

# Fatality ratio can be calculated by dividing between the `deaths` and `confirmed_cases` columns.

# In[8]:


covid_merge["fatality_ratio"] = covid_merge["deaths"]/covid_merge["confirmed_cases"]
print(covid_merge.head())


# ### Countries with the Highest Fatality Ratio

# In[9]:


top_20_fatality_rate = covid_merge.sort_values(by='fatality_ratio', ascending=False).head(20)
print(top_20_fatality_rate[["geo_id","country_name","fatality_ratio"]])


# ### The Highest Fatality Ratio in August 2020

# In[10]:


# Number of cases in august
covid_merge_august = covid_merge.loc["2020-08"].groupby("country_name").sum()
# Calculating fatality ratio in august
covid_merge_august["fatality_ratio"] = covid_merge_august["deaths"]/covid_merge_august["confirmed_cases"]
# Countries with the highest fatality ratio in august
top_20_fatality_rate_on_august = covid_merge_august.sort_values(by="fatality_ratio", ascending=False).head(20)
print("Countries with the Highest Fatality Ratio in August 2020:\n",top_20_fatality_rate_on_august["fatality_ratio"])


# ### Visualization of the Country with the Highest Fatality Ratio in August 2020

# In[11]:


# Import libraries
import matplotlib.pyplot as plt
import seaborn as sns


# In[12]:


plt.figure(figsize=(8,8))
top_20_fatality_rate_on_august["fatality_ratio"].sort_values().plot(kind="barh", color="steelblue")
plt.title("Top 20 Highest Fatality Rate Countries", fontsize=18, color="k")
plt.xlabel("Fatality Rate", fontsize=14)
plt.ylabel("Country Name", fontsize=14)
plt.grid(axis="x")
plt.tight_layout()
plt.show()


# It can be seen that Yemen has the largest fatality ratio compared to other countries in August 2020.

# ### COVID-19 Case in ASEAN 

# In[13]:


asean_country_id = ["ID", "MY", "SG", "TH", "VN"]
filter_list = [(covid_merge["geo_id"]==country_id).to_numpy() for country_id in asean_country_id]
filter_array = np.column_stack(filter_list).sum(axis=1, dtype="bool")
covid_merge_asean = covid_merge[filter_array].sort_index()

print("Check unique value in column 'country_name':", covid_merge_asean["country_name"].unique())
print(covid_merge_asean.head())


# ### When was the First Case of COVID-19 Popped Up in ASEAN?

# In[14]:


print("The first case popped up in ASEAN countries:")
for country_id in asean_country_id:
    asean_country = covid_merge_asean[covid_merge_asean["geo_id"]==country_id]
    first_case = asean_country[asean_country["confirmed_cases"]>0][["confirmed_cases","geo_id","country_name"]]
print(first_case.head(1))


# ### Covid-19 cases in March 2020

# In[15]:


covid_merge_asean_march_onward = covid_merge_asean[covid_merge_asean.index>="2020-03-01"]
print(covid_merge_asean_march_onward.head())


# ### Visualization of COVID-19 Cases in ASEAN

# In[16]:


plt.figure(figsize=(16,8))
sns.lineplot(data=covid_merge_asean_march_onward,
x=covid_merge_asean_march_onward.index,
y="confirmed_cases",
hue="country_name",
linewidth=2)
plt.xlabel('Record Date', fontsize=14)
plt.ylabel('Total Cases', fontsize=14)
plt.title('Comparison of COVID19 Cases in 5 ASEAN Countries', color="k", fontsize=18)
plt.grid()
plt.tight_layout()
plt.show()


# It can be seen that Indonesia has experienced a large increase in Covid-19 cases compared to other ASEAN countries. It is also seen that the country that has the lowest increase in the number of Covid-19 cases are Vietnam and Thailand.
