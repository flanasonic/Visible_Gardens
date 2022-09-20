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
# Argparse code for running initdb with command line args
# this kinda has to be at the beginning
#  
#  When you want to refresh your local CSV files in the data
#  folder with the contents of your google sheet document:
#  python ./initdb.py --update all 
#  or
#  python ./initdb.py --update [sheet name]
#####################################################################

sheet_names = [
    'company',
    'address',
    'product',
    'facility'
]

# use argparse module to parse command like args for initdb
# this will let us add command line arguments to our program
# so we can (optionally) do things like update our local csv
# data from the contents of our google sheets worksheets
arg_parser = argparse.ArgumentParser(description="backup CSVs and replace")
arg_parser.add_argument("-update", action="store")
# you can add more lines like the one immediately above when you want to create
# more arguments
args = vars(arg_parser.parse_args())

if args.get('update', False):
    # the name we were given with the -update flag
    # probably something like company or product
    thing_name = args['update']
    print(
        f"We're going to update our {args['update']} data from google sheets")

    # Make sure we have a data dir and a backup dir
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
    Given a company name, find an the first matching record from the spreadsheet
    where the trade name matches. Return a model object created from this record
    """

    # Use pandas DataFrame.query to find address records in the spreadsheet
    # where the company trade name matches
    df_matching = df_to_search.query(f" {join_column_name} == '{join_column_value}' ")
    if df_matching.shape[0] >= 1:
        # we found at least one matching row - we'll add the first/only one found
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
    Given a company name, find products in the spreadsheet where the company_trade_name matches.
    Return a list of Product objects we can insert.
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
engine = create_engine(DB_URI)
print("Dropping tables!!!!!")
db.metadata.drop_all(engine)  # drop all tables

print("Creating tables!")
db.metadata.create_all(engine)  # now create all tables


#####################################################################
# Code that reads our CSV data and inserts into the database
#####################################################################

# Now that we have a bunch of useful functions defined for working with our
# Google Sheets, let's download each worksheet as a csv and load using pandas
# into a DataFrame
df_company_sheet = pd.read_csv('./data/company.csv')
df_product_sheet = pd.read_csv('./data/product.csv')
df_address_sheet = pd.read_csv('./data/address.csv')
df_facility_sheet = pd.read_csv('./data/facility.csv')

# we need to clean some of the raw data coming in from our sheet: we'll
# start by making sure each field in each column conforms to a dtype that
# is compatible with the column type of our database table.  This should
# also apply pandas NA/NaN where we had blank cells in order to represent
# NULL in our database table columns that are optional/nullable.
df_company_sheet['for_profit'] = df_company_sheet['for_profit'].astype(bool)

df_company_sheet['parent_id'] = df_company_sheet['parent_id'].astype("Int32")

# Next...
# Find the field names that are both in the spreadsheet and names of columns
# in our company table - we have extra columns in some sheets that can't go
# in the table - and some ID columns in the table that are not in the sheet.
# So filter these out and return a list of just the column names that appear
# in both.
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


with Session(engine) as session:

    # Now, iterate over each row in the company sheet and find the
    # products, addresses, and facilities for each one and insert them into
    # the database
    # the variable company_row in the following line will be a namedtuple
    # of the dataframe row - each time it iterates to the next row:
    # https://docs.python.org/3/library/collections.html#collections.namedtuple
    for company_row in df_company_sheet[company_fields].itertuples(index=False):

        # convert the row from the company sheet to a dict
        # namedtuple has a function _asdict() that converts itself into a dict
        company_fields = company_row._asdict()
        new_company = Company(**company_fields)

        new_company.address = find_first_matching('company_trade_name',
                                                  new_company.trade_name,
                                                  df_address_sheet,
                                                  address_fields,
                                                  Address)

        new_company.products = find_all_matching('company_trade_name',
                                                 new_company.trade_name,
                                                 df_product_sheet,
                                                 product_fields,
                                                 Product)

        new_company.facilities = find_all_matching('company_trade_name',
                                                 new_company.trade_name,
                                                 df_facility_sheet,
                                                 facility_fields,
                                                 Facility)

        session.add(new_company)

    # Leaving this here for reference - if we want to load a csv into a table
    # individially...
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

    try:
        session.commit()
    except DBAPIError as err:
        print(f"  !!! ERROR: {err}")

