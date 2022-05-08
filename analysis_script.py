# %% [markdown]
# # Workflow

import os

# %%
# imports
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

# %%
price_ap_data = pd.read_excel(price_app_filepath)
price_ap_data.head()

# %%
price_hous_data = pd.read_excel(price_house_filepath)
price_hous_data.head()

# %%
rent_ap_data = pd.read_excel(rent_ap_filepath)
rent_ap_data.head()

# %%
reg_price_data = pd.read_excel(reg_price_filepath)
reg_price_data.head()

# %%
# TODO correct the reg prices
# TODO check types
# TODO check null
# TODO weird stuff
# TODO understand which fields connect to different tables
# TODO pay attention to different levels of aggregation

# %%
