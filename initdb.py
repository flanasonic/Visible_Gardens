from typing import ClassVar, List
from model import Company, Address, Product, Facility
from model import db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
import pandas as pd
import argparse
import os
from db_utils import download_google_worksheet, backup_data_file, get_matching_column_names


#####################################################################
# Setup/Configuraton
#####################################################################

# TODO: get DB_URI from a config
from server import DB_URI

# The ID of our google sheets document see the "sharing url" to find this
GSHEET_ID = "1IXViZcOCmt5ZO-QJBKQ0HUjwna52Vnr6_WcMlQbpCp4"

#####################################################################
# argparse code for running initdb.py with command line args
# (needs to be at the beginning)
#  
# these command line args let us refresh our local CSV files in the 
# data folder with the contents of our google sheet document:
#  $ python ./initdb.py -update all 
#  $ python ./initdb.py -update [sheet name]
#####################################################################

sheet_names = [
    'company',
    'address',
    'product',
    'facility'
]

# this code lets us add command line arguments to our program
# so we can do things like update our local CSV data from the 
# contents of our google sheets worksheets
arg_parser = argparse.ArgumentParser(description="backup CSVs and replace")
arg_parser.add_argument("-update", action="store")
# you can add more 'add_argument' lines like the one immediately 
# above when you want to create more arguments
args = vars(arg_parser.parse_args())

if args.get('update', False):
    # the name we were given with the -update flag
    # probably something like 'company' or 'product'
    thing_name = args['update']
    # print(
    # f"We're going to update our {args['update']} data from google sheets")

    # this makes sure we have a data dir and a backup dir
    os.makedirs("./data/backup", exist_ok=True)

    if thing_name == "all":
        for sheet_name in sheet_names:
            backup_data_file(sheet_name)
            download_google_worksheet(GSHEET_ID, sheet_name)
    else:
        backup_data_file(thing_name)
        download_google_worksheet(GSHEET_ID, thing_name)


#####################################################################
# Functions for finding rows we need in csv files / worksheets
#####################################################################


def find_first_matching(join_column_value: str, # column value to look for 
                        df_to_search: pd.DataFrame, # daframe to look in
                        join_column_name: str, # column name to look in
                        columns: List[str], # cols to use when creating a result
                        _class: db.Model, # class type of object to create
                        query: str=None
                        ):


    """
    Function takes in a value, a dataframe to search, the column name to search, 
    and a lst of columns to return as a result and creates an object of type
    specified  
    """

    # Use pandas DataFrame.query to find address records in the spreadsheet
    # where the company trade name matches
    df_matching = df_to_search.query(f" {join_column_name} == '{join_column_value}' ")
    if query: 
        df_matching = df_matching.query(query)
    if df_matching.shape[0] >= 1:
        # we found at least one matching row - we'll add the first/only one found
        # pandas iloc[] function lets us select rows by index
        row = df_matching.iloc[0]
        address_fields_dict = row[columns].to_dict()
        return _class(**address_fields_dict)
    else:
        print(f"   !!! !!! No {_class.__name__} found for {join_column_value} !!! !!!")



# def find_all_matching(join_column_name: str,
#                       join_column_value: str,
#                       df_to_search: pd.DataFrame,
#                       columns: List[str],
#                       _class: db.Model
#                       ):
#


def find_all_matching(join_column_value: str, #  value to look for 
                        df_to_search: pd.DataFrame, # daframe to look for it in
                        join_column_name: str, # column name to look in
                        columns: List[str], # cols to use when creating a result
                        _class: db.Model # class type of object to create
                        ):


    """
    Given a company name, find products in the spreadsheet where the company_trade_name matches.
    Return a list of Product objects we can insert.
    """
    # initialize an empty list to return
    result = []

    if join_column_name not in df_to_search.columns.values:
        print(f"!!!!!!! {_class.__name__} : Join column not found!  Columns:")
        return

    df_matching = df_to_search.query(f"{join_column_name} == '{join_column_value}'")

    for row in df_matching[columns].itertuples(index=False):
        fields_dict = row._asdict()
        result.append(_class(**fields_dict))

    return result


#####################################################################
# Code that drops/creates tables in the database
#####################################################################

# Note: we just want to talk to our db right now and don't yet need
# to start up Flask, so instead of using Flask SQLalchemy to make the 
# db connection, we're using regular SQLAlchemy's create_engine 
# function to create en engine object, info here:
# https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine(DB_URI)

# We'll use SQL Alchemy's metadata object here to drop and create
# our tables
# https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#tutorial-working-with-metadata
print("Dropping tables!!!!!")
db.metadata.drop_all(engine)  
print("Creating tables!")
db.metadata.create_all(engine)  


#####################################################################
# Code that reads our CSV as pandas dataframes
# 
# Pandas is helpful here because our data needs cleaning
# We'll have even greater need for it in the future when we build out
# our data model further and bring in geospatial data from an API
#####################################################################

# load our CSV files as pandas DataFrames
df_company_sheet = pd.read_csv('./data/company.csv')
df_facility_sheet = pd.read_csv('./data/facility.csv')
df_product_sheet = pd.read_csv('./data/product.csv')
dtypes = {"postal" : "object"}
df_address_sheet = pd.read_csv('./data/address.csv', dtype=dtypes)
# dtypes = {"latitude" : "float64", "longitude" : "float64"}
df_locations_sheet = pd.read_csv('./data/locations.csv', names=["nickname", "latitude", "longitude"])
df_address_sheet = df_address_sheet.merge(df_locations_sheet, on="nickname", how="left")



#####################################################################
# Code that cleans our pandas dataframes 
#
# First, makes sure each field in each column conforms to a dtype 
# that is compatible with the column type of our database table

#####################################################################


df_company_sheet['for_profit'] = df_company_sheet['for_profit'].astype(bool)
df_company_sheet['parent_id'] = df_company_sheet['parent_id'].astype("Int32")
# df_company_sheet['total_employees'] = df_company_sheet['total_employees'].astype("Int32")


# Also apply pandas NA/NaN where we had blank cells in order to represent
# NULL in our database table columns that are optional/nullable.


#####################################################################
# Code that creates a list of columns common to our spreadsheet and tables
#
# It filters out any that aren't common
# (We need to do this because we have extra columns in some sheets 
# that can't go into our tables, plus some ID columns in tables that 
# are not in our sheets.)


#####################################################################

# function 'get_matching_column_names' is defined in db_utils
company_fields = get_matching_column_names(df_company_sheet, 'company', db)
facility_fields = get_matching_column_names(df_facility_sheet, 'facility', db)
address_fields = get_matching_column_names(df_address_sheet, 'address', db)
product_fields = get_matching_column_names(df_product_sheet, 'product', db)
# print(f"matching fields for product: {product_fields}")
# print("")


#####################################################################
# Code that populates our database with data from our clean pandas
# DataFrames 
#####################################################################

# note - using the sqlachemy.orm Session class, so our session syntax 
# is slightly different than that of flask sqlalchemy (we use the below 
# instead of model.db.session.add_all(...) and model.db.session.commit() )
with Session(engine) as session:

    # Taking just the columns we want from df_company_sheet, iterate 
    # over each row and create from it a namedtuple
    # Store that namedtuple in variable 'company_row' 
    # https://docs.python.org/3/library/collections.html#collections.namedtuple
    for company_row in df_company_sheet[company_fields].itertuples(index=False):

        # now use namedtuple's function _asdict() to convert each company_row 
        # tuple into a dict
        # NOTE: each key in this dict will be the column name we used in our
        # gsheet and will go into our db table, the value is the val in each col
        # for that row
        company_fields = company_row._asdict()

        # now let's construct a new Company object
        # because class Company extends SQLAlchemy Model (db.Model) it can take
        # kwargs 
        # we'll use the value of any key in the kwargs that matches a 
        # Company atttribute as the value of that attribute
        new_company = Company(**company_fields) #  unpacks company_fields dict
     
        new_company.address = find_first_matching(new_company.trade_name,
                                                 df_address_sheet,
                                                 'company_trade_name',
                                                 address_fields,
                                                 Address,
                                                 "make_default==True")

        # use function 'find_all_matching' (line 121) to populate the company
        # object with products 
        new_company.products = find_all_matching(new_company.trade_name, # value to search for
                                                df_product_sheet, # df to look in
                                                'company_trade_name', # col to look in
                                                product_fields, # columns to take for result
                                                Product) # create a Product object

 
        # now populate the company object with facilities 
        new_company.facilities = find_all_matching(new_company.trade_name, # value to search for
                                                df_facility_sheet, # df to look in
                                                'company_trade_name', # col to look in
                                                facility_fields, # columns to take for result
                                                Facility) # create a Facility object

        

        # now populate each of the company's facilities with an address
        for facility in new_company.facilities:
            facility.address = find_first_matching(facility.nickname, # value to search for
                                                df_address_sheet, # df to look in
                                                'nickname', # col name to look in
                                                address_fields, #  cols to take for result
                                                Address) # object type to create
 
        session.add(new_company)

#####################################################################
# Code to individually drop/create a table in the database
#####################################################################

    # In case we want to load a csv into a table individually...
    # for address_row in df_address_sheet[address_fields].itertuples(index=False):
    #     # convert the row from the address sheet to a dict
    #     address_fields = address_row._asdict()
    #     session.add( Address(**address_fields) )

    # for product_row in df_product_sheet[product_fields].itertuples(index=False):
    #     # convert the row from the address sheet to a dict
    #     product_fields = product_row._asdict()
    #     session.add( Product(**product_fields) )

    # for facility_row in df_facility_sheet[facility_fields].itertuples(index=False):
    #     # convert the row from the address sheet to a dict
    #     facility_fields = facility_row._asdict()
    #     session.add( Facility(**facility_fields) )


#####################################################################

    try:
        session.commit()
    except DBAPIError as err:
        print(f"  !!! ERROR: {err}")

   


