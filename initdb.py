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
    # probably something like company or product
    thing_name = args['update']
    print(
        f"We're going to update our {args['update']} data from google sheets")

    # this make ssure we have a data dir and a backup dir
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

def find_first_matching(join_column_name: str, # column name to look for a match
                        join_column_value: str, # value to look for in that col
                        df_to_search: pd.DataFrame, # daframe to look in
                        columns: List[str], # cols to use when creating a result
                        _class: db.Model # model obj - call this constructor and return it
                        ):
    """
    Given a company name, find the first matching record from the spreadsheet
    where trade_name matches. Return a model object created from this record
    """

    # Use pandas DataFrame.query to find address records in the spreadsheet
    # where the company trade name matches
    df_matching = df_to_search.query(f" {join_column_name} == '{join_column_value}' ")
    if df_matching.shape[0] >= 1:
        # we found at least one matching row - we'll add the first/only one found
        # pandas iloc[] function lets us select rows by index
        row = df_matching.iloc[0]
        address_fields_dict = row[columns].to_dict()
        return _class(**address_fields_dict)
    else:
        print(f"   !!! !!! No {_class.__name__} found for {join_column_value} !!! !!!")


def find_all_matching(join_column_name: str,
                      join_column_value: str,
                      df_to_search: pd.DataFrame,
                      columns: List[str],
                      _class: db.Model):
    """
    Given a company name, find products in the spreadsheet where the company_trade_name matches.Return a list of Product objects we can insert.
    """
    # initialize an empty list to return
    result = []

    if join_column_name not in df_to_search.columns.values:
        print(f"!!!!!!! {_class.__name__} : Join column not found!  Columns:")
        print(df_to_search.columns)
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

# Note: instead of using os.system('dropdb ...') and ('createdb ...') 
# we're using SQL Alchemy's metadata object here to drop our tables
print("Dropping tables!!!!!")
db.metadata.drop_all(engine)  
print("Creating tables!")
db.metadata.create_all(engine)  # now create all tables


#####################################################################
# Code that reads our CSV data as pandas dataframes, so we can 
# inserts the data into our database
# pandas is helpful here because our data needs cleaning and because 
# we'll have even greater need for it in the future when we build out
# our data model further and bring in geospatial data from an API
#####################################################################

# let take each CSV file we downloaded from google sheets
# load it into a pandas DataFrame
df_company_sheet = pd.read_csv('./data/company.csv')
df_product_sheet = pd.read_csv('./data/product.csv')
df_address_sheet = pd.read_csv('./data/address.csv')
df_facility_sheet = pd.read_csv('./data/facility.csv')


#####################################################################
# Code that cleans our pandas dataframes 
# Starts by making sure dtypes are compatible with our database tables
# Then look for columns that appear in both our spreadsheet and tables
# and filters out any that aren't common
#####################################################################

# Let's make sure each field in each column conforms to a dtype that
# is compatible with the column type of our database table
# Also apply pandas NA/NaN where we had blank cells in order to represent
# NULL in our database table columns that are optional/nullable.
df_company_sheet['for_profit'] = df_company_sheet['for_profit'].astype(bool)
df_company_sheet['parent_id'] = df_company_sheet['parent_id'].astype("Int32")

# Now, find the field names that are common to our spreadsheet and table
# column names and filter out any that don't match
# We need to do this ecause we have extra columns in some sheets 
# that can't go in the table, plus some ID columns in the table that 
# are not in the sheet.
company_fields = get_matching_column_names(df_company_sheet, 'company', db)
print(f"list of matching fields for company: {company_fields}")
print("")

address_fields = get_matching_column_names(df_address_sheet, 'address', db)
print(f"list of matching fields for address: {address_fields}")
print("")

product_fields = get_matching_column_names(df_product_sheet, 'product', db)
print(f"list of matching fields for product: {product_fields}")
print("")

facility_fields = get_matching_column_names(df_facility_sheet, 'facility', db)
print(f"list of matching fields for facility: {facility_fields}")
print("")


#####################################################################
# Code that populates our database with data from our clean pandas
# dataframes 
#####################################################################

# using SQLAlchemy's Session class here instead of flask sqlalchemy
with Session(engine) as session:

    # Iterate over each row in df_company_sheet and find the
    # products, addresses, and facilities for each and insert them into
    # our database
    # TODO: further understand namedtupe and function .itertuples
    # The variable 'company_row' in the following line will be a namedtuple
    # of the dataframe row - each time it iterates to the next row:
    # https://docs.python.org/3/library/collections.html#collections.namedtuple
    for company_row in df_company_sheet[company_fields].itertuples(index=False):

        # convert the row from the company sheet to a dict
        # namedtuple has a function called _asdict() that converts 
        # itself into a dict
        company_fields = company_row._asdict()
        # TODO: further understand syntax **company_fields
        new_company = Company(**company_fields)

        # relationships - address, products, facilities at once and
        # makes sure they are all linked

        # the code below uses function 'find_first_matching' (see line 72)
        # to populate a company object with an address - it looks in
        # dataframe 'df_address_sheet' in the 'company_trade_name' column
        # for the given company name and takes the first address with a match
        new_company.address = find_first_matching('company_trade_name',
                                                  new_company.trade_name,
                                                  df_address_sheet,
                                                  address_fields,
                                                  Address)

        # code below uses function 'find_all_matching' (see line 96) to 
        # populate a company object with products - it looks in 
        # 'df_product_sheet' in column 'company_trade_name' for the given
        # company name and takes all products that match
        new_company.products = find_all_matching('company_trade_name',
                                                 new_company.trade_name,
                                                 df_product_sheet,
                                                 product_fields,
                                                 Product)

        # works same as the above, but searches for facilities 
        # that match the given company name
        new_company.facilities = find_all_matching('company_trade_name',
                                                 new_company.trade_name,
                                                 df_facility_sheet,
                                                 facility_fields,
                                                 Facility)

    # again, we are using SQLAlchemy's Session class, rather than Flask 
    # SQL Alchemy, so our session syntax is slightly different (we use 
    # the below instead of model.db.session.add_all(...) and 
    # model.db.session.commit()
        session.add(new_company)

#####################################################################
# Code to individually drop/create a table in the database
#####################################################################

    # Leaving this here for reference - in case we want to load a csv 
    # into a table individually...
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

