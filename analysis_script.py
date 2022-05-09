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

price_app_filepath = (
    filepath + "/datasets/announced-prices-apartments-luxembourg-city.xlsx"
)
price_house_filepath = (
    filepath + "/datasets/announced-prices-houses-luxembourg-city.xlsx"
)
rent_ap_filepath = filepath + "/datasets/announced-rent-apartments-luxembourg-city.xlsx"
reg_price_filepath = (
    filepath + "/datasets/registered-prices-apartements-by-commune.xlsx"
)

# %% [markdown]
# We open the dataset and start working on the indexing, organizing the data by Quarter and Year.
# Since the 3 datasets are similar we can create a function to avoid repeating code.

# %%
def clean_index(dataset):
    # ordering the data by quarter and year, creating a multi-index
    arrays = [[*dataset.Quarter], [*dataset.Year]]

    tuples = list(zip(*arrays))

    index = pd.MultiIndex.from_tuples(tuples, names=["Quarter", "Year"])

    dataset.set_index(index, inplace=True)

    # we don't need the quarter and year since they are part  of the index
    dataset.drop(columns=["Quarter", "Year"], inplace=True)

    dataset.sort_index(inplace=True)

    dataset.drop(index="Luxembourg City", inplace=True)
    dataset.drop(index="National Average", inplace=True)


# %% [markdown]
# We start checking the datatype and we start handling the NaN.

# %%
def check_type_missing(dataset, missing, rent=None):
    col1 = "Number of offers"
    col2 = "Average announced price in €"
    col3 = "Average announced price per squared meter in €"

    if rent:
        col2 = "Average announced rent in €"
        col3 = "Average announced rent per squared meter in €"

    # easy handling of missing data, may change for better modeling
    val = missing
    dataset.replace("*", val, inplace=True)
    dataset[col1] = dataset[col1].astype("int64")
    dataset[col2] = dataset[col2].astype("float64")
    dataset[col3] = dataset[col3].astype("float64")

    # type check
    print(
        f"{col1 + ':':<50} \
        {str(dataset[col1].dtype)}"
    )
    print(
        f"{col2 + ':':<50} \
        {str(dataset[col2].dtype)}"
    )
    print(
        f"{col3 + ':':<50} \
        {str(dataset[col3].dtype)}"
    )


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
check_type_missing(rent_ap_data, 0, rent=any)
rent_ap_data

# %%
reg_price_data = pd.read_excel(reg_price_filepath)
reg_price_data

# %%
# TODO correct the reg prices
# TODO check types
# TODO check null
# TODO weird stuff
# TODO understand which fields connect to different tables
# TODO pay attention to different levels of aggregation

# %%
