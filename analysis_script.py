# %% [markdown]
# # Workflow

# %%
# imports
import os

import numpy as np
import pandas as pd

# %%
# Paths to the files
filepath = os.getcwd()

price_app_filepath = filepath + "/datasets/announced-prices-apartments-luxembourg-city.xlsx"
price_house_filepath = filepath + "/datasets/announced-prices-houses-luxembourg-city.xlsx"
rent_ap_filepath = filepath + "/datasets/announced-rent-apartments-luxembourg-city.xlsx"
reg_price_filepath = filepath + "/datasets/registered-prices-apartements-by-commune.xlsx"

# %% [markdown]
# We open the dataset and start working on the indexing, organizing the data by Quarter and Year.
# Since the first 3 datasets are similar we can create a function to avoid repeating code.

# %%
def clean_index(dataset):
    # ordering the data by quarter and year, creating a multi-index
    arrays = [[*dataset.Quarter], [*dataset.Year]]

    tuples = list(zip(*arrays))

    index =pd.MultiIndex.from_tuples(tuples, names=['Quarter', 'Year'])

    dataset.set_index(index, inplace=True)

    # we don't need the quarter and year since they are part  of the index
    dataset.drop(columns=['Quarter', 'Year'], inplace=True)

    dataset.sort_index(inplace=True)

    # we don't want to waste any data so we will return these info
    ret = [dataset.loc['Luxembourg City'], dataset.loc['National Average']]

    dataset.drop(index='Luxembourg City', inplace=True)
    dataset.drop(index='National Average', inplace=True)

    return ret

# %% [markdown]
# After we cleaned the data we check the datatype and we handle the missing that.

# %%
def check_type_missing(dataset, missing, rent=None):
    col1 = 'Number of offers'
    col2 = 'Average announced price in €'
    col3 = 'Average announced price per squared meter in €'

    if rent:
        col2 = 'Average announced rent in €'
        col3 = 'Average announced rent per squared meter in €'

    # easy handling of missing data, may change for better modeling
    val = missing
    dataset.replace('*', val, inplace=True)
    dataset.loc[:,col1] = dataset.loc[:,col1].astype('int64')
    dataset.loc[:,col2] = dataset.loc[:,col2].astype('float64').round(2)
    dataset.loc[:,col3] = dataset.loc[:,col3].astype('float64').round(2)

    # type check
    print(f"{col1 + ':':<50} \
        {str(dataset.loc[:,col1].dtype)}")
    print(f"{col2 + ':':<50} \
        {str(dataset.loc[:,col2].dtype)}")
    print(f"{col3 + ':':<50} \
        {str(dataset.loc[:,col3].dtype)}")

# %% [markdown]
# We aply the functions we've defined on the first 3 datasets.

# %%
# acquiring the data
price_ap_data = pd.read_excel(price_app_filepath)

price_ap_data

# %%

# cleaning the indexing
temp =  clean_index(price_ap_data)
d1_lux_avg = temp[0]
d1_nat_avg = temp[1]

print(d1_lux_avg)
print(d1_nat_avg)

price_ap_data

# %%
# checking the types and handling missing values
check_type_missing(price_ap_data, 0)
price_ap_data

# %%
# acquiring the data
price_hous_data = pd.read_excel(price_house_filepath)

# cleaning the indexing
temp = clean_index(price_hous_data)

d2_lux_avg = temp[0]
d2_nat_avg = temp[1]

print(d2_lux_avg)
print(d2_nat_avg)

price_hous_data.head()

# %%
# checking types and handling missing data
check_type_missing(price_hous_data, 0)
price_hous_data

# %%
# acquiring the data
rent_ap_data = pd.read_excel(rent_ap_filepath)

# cleaning the indexing
temp = clean_index(rent_ap_data)

d3_lux_avg = temp[0]
d3_nat_avg = temp[1]

print(d3_lux_avg)
print(d3_nat_avg)

rent_ap_data.head()

# %%
check_type_missing(rent_ap_data, 0, rent=True)
rent_ap_data

# %%
reg_price_data = pd.read_excel(reg_price_filepath)
reg_price_data

# %%
tuples1 = []
for el in reg_price_data.iloc[0, 1:4]:
    tuples1.append(("Constructed", el))
for el in reg_price_data.iloc[0, 1:4]:
    tuples1.append(("VEFA", el))

print(tuples1)

new_header = reg_price_data.iloc[0]
reg_price_data.columns = new_header
reg_price_data = reg_price_data.iloc[1:]

reg_price_data

# %%
# ordering the data by Commune and year, creating a multi-index
arrays = [[*reg_price_data.loc[:,'Commune']], [*reg_price_data.loc[:,'Year']]]
tuples = list(zip(*arrays))

index =pd.MultiIndex.from_tuples(tuples, names=['Commune', 'Year'])
reg_price_data.set_index(index, inplace=True)

# we don't need the Commune and year since they are part  of the index
reg_price_data.drop(columns=['Commune', 'Year'], inplace=True)

reg_price_data.sort_index(inplace=True)

d4_nat_avg = reg_price_data.loc['National Average']
# print(d4_nat_avg)

reg_price_data.drop(index='National Average', inplace=True)

new_columns = pd.MultiIndex.from_tuples(tuples1, names=["Construction State", "Detail"])
reg_price_data.columns = new_columns

reg_price_data

# %%
reg_price_data.loc[:,("Constructed", "Price range for price per squared meter")]
# TODO #2 parse the range constructed
# TODO #3 parse the range VEFA

# %%



