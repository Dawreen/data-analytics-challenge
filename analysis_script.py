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
# Since the 3 datasets are similar we can create a function to avoid repeating code.

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

    dataset.drop(index='Luxembourg City', inplace=True)
    dataset.drop(index='National Average', inplace=True)

# %% [markdown]
# We start checking the datatype and we start handling the NaN.

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
    dataset[col1] = dataset[col1].astype('int64')
    dataset[col2] = dataset[col2].astype('float64').round(2)
    dataset[col3] = dataset[col3].astype('float64').round(2)

    # type check
    print(f"{col1 + ':':<50} \
        {str(dataset[col1].dtype)}")
    print(f"{col2 + ':':<50} \
        {str(dataset[col2].dtype)}")
    print(f"{col3 + ':':<50} \
        {str(dataset[col3].dtype)}")

# %%
# acquiring the data
price_ap_data = pd.read_excel(price_app_filepath)

# cleaning the indexing
clean_index(price_ap_data)

price_ap_data


# %%
# checking the types and handling missing values
check_type_missing(price_ap_data, 0)
price_ap_data

# %%
# acquiring the data
price_hous_data = pd.read_excel(price_house_filepath)

# clening the indexing
clean_index(price_hous_data)

price_hous_data.head()

# %%
# checking types and handling missing data
check_type_missing(price_hous_data, 0)
price_hous_data

# %%
# acquiring the data
rent_ap_data = pd.read_excel(rent_ap_filepath)

# cleaning the indexing
clean_index(rent_ap_data)

rent_ap_data.head()

# %%
check_type_missing(rent_ap_data, 0, rent=True)
rent_ap_data

# %%
reg_price_data = pd.read_excel(reg_price_filepath)
reg_price_data

# %%
tuples1 = []
for el in reg_price_data.iloc[0][1:4]:
    tuples1.append(("Constructed", el))
for el in reg_price_data.iloc[0][1:4]:
    tuples1.append(("VEFA", el))

print(tuples1)

new_header = reg_price_data.iloc[0]
reg_price_data.columns = new_header
reg_price_data = reg_price_data[1:]

reg_price_data

# %%
# ordering the data by quarter and year, creating a multi-index
arrays = [[*reg_price_data['Commune']], [*reg_price_data.Year]]
tuples = list(zip(*arrays))
index =pd.MultiIndex.from_tuples(tuples, names=['Commune', 'Year'])
reg_price_data.set_index(index, inplace=True)

# we don't need the Commune and year since they are part  of the index
reg_price_data.drop(columns=['Commune', 'Year'], inplace=True)

reg_price_data.sort_index(inplace=True)
reg_price_data.drop(index='National Average', inplace=True)

index = pd.MultiIndex.from_tuples(tuples1, names=["Construction State", "Detail"])
reg_price_data.columns = index

reg_price_data

# %%
reg_price_data.loc[:]["Constructed", "Price range for price per squared meter"]
# TODO #2 parse the range constructed
# TODO #3 parse the range VEFA


