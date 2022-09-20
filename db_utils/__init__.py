import psycopg2
import shutil
import urllib
import os
import numpy as np
import pandas as pd


def download_google_worksheet(doc_id, sheet_name):
    """
        Given a string with a sheet name, make a URL for downloading that sheet from 
        our Project_Database spreadsheet as a CSV file. We'll give this URL to 
        to urllib2 and have it save the csv in our data folder

        The id of our Google Sheets doc (from the 'Share' button??)
        Browser link to doc: 
        https://docs.google.com/spreadsheets/d/1IXViZcOCmt5ZO-QJBKQ0HUjwna52Vnr6_WcMlQbpCp4/
    """
    csv_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

    print(f"Getting {sheet_name} sheet data using URL: {csv_url}")
    with urllib.request.urlopen(csv_url) as gsheet:
        with open(f"./data/{sheet_name}.csv", "wb") as file:
            file.write(gsheet.read())


def backup_data_file(file_name):
    # Check if we have files to back up
    existing_filename = f"./data/{file_name}.csv"
    if os.path.exists(existing_filename):
        print(f"Backing up existing data: {existing_filename} to ./data/backup")
        backup_filename = f"./data/backup/{file_name}.csv"
        shutil.move(existing_filename ,backup_filename)


def get_matching_column_names(sheet_df, table_name, db):
    """ 
    Arguments:
        sheet_df - a pandas dataframe containing our google sheet data
        table_name - a string with the name of our table
        db - our flask sqlalchemy "db"

    Look at the list of columns in our spreadsheet vs. columns in our table 
    and find the intersection. This way, we can filter out any spreadsheet 
    columns that don't belong in the table and keep just the column names in 
    the spreadsheet that match the column names in the table. 
    """
    spreadsheet_cols = sheet_df.columns.to_list()

    table_cols = [column.name for column in db.metadata.tables[table_name].columns]
    
    # print(list(set(spreadsheet_cols) & set(table_cols)))
    # print(" ")
    return list(set(spreadsheet_cols) & set(table_cols))


PSYCOPG2_NULL = psycopg2.extensions.AsIs('NULL')
PSYCOPG2_FLOAT = psycopg2.extensions.Float

def float_handler_with_nan_to_null(float_or_nan):
    """
    A custom data type handler for psycopg2 that will treat pandas NA/NaN as
    NULL when talking to postgres:

    to use:
    psycopg2.extensions.register_adapter(float, float_handler_with_nan_to_null)
    
    IMPORT DATA FROM CSV
    We're importing data into our database that came from a spreadsheet. We
    want to treat blank cells in each worksheet as NULL values in our 
    database. This will work wherever we have defined our database columns as 
    nullable (not defined with nullable=False.)
    
    CONVERT CSV USING PANDAS...
    We're using pandas to convert our data from CSV (downloaded from our google 
    sheet) into data types compatible with those of our database table columns. 
    Pandas uses NA/NaN to represent blanks in columns that otherwise have values 
    of a specific dtype object or int32 or float.
    

    PSYCOPG ADAPTER FUNCTION...
    We're using psycopg2 to talk to our database - (sqlalchemy is using psycopg2)
    Unfortunately, psycopg2 doesn't understand what pandas NA/NaN values 
    are, so it will throw an error if we tell it to convert one into something 
    postgres understands. 
    
    So we need to give psycopg an "adapter function" that 
    knows how to do the conversion.Here's how it works: We have some code below 
    that transforms rows from our dataframes into sqlalchemy model objects. 
    
    Example - we make a Company object and insert it into the database. When 
    we do this, we're giving the Company constructor the row of data from the 
    company dataframe. To do this, we convert the row into a dict and then 
    unpack it in the call to the Company constructor: 
        company_to_insert = Company(**dict_of_dataframe_row)
    
    Once we've created the company_to_insert, we give it to sqlalchemy and tell 
    it to insert it into the database: 
        session.add(company_to_insert)

    We then need to tell SQLAlchemy to give psycopg2 the data inside the
    objects we added, company_to_insert, using session.add() and convert that 
    data to something PostgreSQL can use to do inserts into our tables:
        session.commit() 
    
    Note - up until we call session.commit() sqlalchemy probably hasn't been 
    talking to our database, it hasn't done anything other than keep a list 
    of the companies we gave it. So, when we get an error involving SQL 
    commands or SQL data types, the error is likely coming from either psycopg2
    or the PostgreSQL database. (Because the conversion didn't happen until we
    called session.commit(), these errors indicate that our code executed all 
    the way through the pandas-to-sqlalchemy-model conversion.)
    
    Our model objects - e.g. class Company(db.Model) define which PostgreSQL
    types each of our table columns should be when we created 
    
    We're relying on psycopg2 to convert our python types to the correct 
    PostgreSQL types. This is not obvious from the code SQLAlchemy wants us 
    to write: Note the SQLAlchemy db.Column() functions and SQLAlchemy type names 
    like db.Integer. For Example, on our Company class we have a total_employees
    column that is an integer that may be null.
    
      total_employees = db.Column(db.Integer)

    This is a convention of SQLAlchemy to communicate that our total_employyes 
    field should be convertable to a Python int or whatever numeric type of our
    database column SQLAlchemy may choose for us after consulting with psycopg2
    about what options are available in PostgreSQL. To find out what the actual 
    PostgreSQL table definition is, we need to read through the SQLAlchemy 
    documentation, the psycopg2 documentation, and the PostgreSQL documentation 
    to piece together the full picture (there has to be a better way!)
    
    Since we're using PostgreSQL, total_employees needs to be convertable to
    a PostgreSQL int type - here's where we can find this information:
    
    SQLAlchemy api doc for db.Integer and friends
    https://docs.sqlalchemy.org/en/14/core/type_basics.html#types-generic
    Note: Also not obvious from the code above nor the documentation - 
    db.Integer means total_employees should be an int or something else to 
    mean Null/None/missing
    
    PostgreSQL doc for numeric types
    https://www.postgresql.org/docs/8.1/datatype.html#DATATYPE-NUMERIC
    
    SQLAlchemy doesn't really know how to talk to PostgreSQL (or any database)
    it relies on libraries (which we could use directly) like psycopg2 to 
    handle things like creating the right INSERT statement for PostgreSQL and 
    converting values into SQL data types for PostgreSQL. So, SQLAlchemy is giving
    psycopg2 data from our Company model objects - and that came from our pandas 
    dataframes - and will contain NA/NaN where we had blanks.
    
    psycopg2 has an extensions feature that allows us to give it functions that
    convert a specific data type in whatever way we want - this will override 
    its default behavior, which will throw an error if it encounters a pandas 
    NA/NaN. https://www.psycopg.org/docs/extensions.html
    
    
    To register one of these functions, we first need to know what kind of data
    type we are converting.  NA/NaN will appear to psycopg2 as a float (see 
    below for why) - and then it's default handler for floats will take a closer 
    look at the value to discover it's actually a pandas NA/NaN type that looks 
    like a float - and raise an error

    pandas, NA/NAN is really a float:
    https://pandas.pydata.org/docs/user_guide/missing_data.html#integer-dtypes-and-missing-data
    
    So, this means we can use psycopg2's "type adaptation protocol" to give it 
    a function to call when it encounetrs things that appear to be floats. 
    This function should return an object that psycopg2 recognizes. We can use
    special psycopg2's classes for Float and Null here. When our function
    returns either a Float or a Null to psycopg2, it then knows how to insert
    it into our into PostgreSQL table using SQL.
    
    In our function, we use an if statement to determine if the float we 
    encountered is a normal float or if it is a NA/NaN and should be converted 
    to Null. For reference, tons of detail on pandas NA vs NaN in links below:
       * https://towardsdatascience.com/nan-none-and-experimental-na-d1f799308dd5
       * https://github.com/pandas-dev/pandas/issues/32265 )
    
      Basically this informs what we could write in our if statement below
      inside the function we'll give psycopg2 to handle floats or NaN
    
    def float_handler_with_nan_to_null():
          if not np.isnan( float_or_nan ):
          ...
    
    The above if statement condition "not np.isnan()" should work for all cases - 
    but may need some tweaking.
    
    The psycopg2 api documentation tells us how to register such a function 
    usingpsycopg2.extensions.register_adapter() for registering data type 
    adapters:
    https://www.psycopg.org/docs/extensions.html#sql-adaptation-protocol-objects
    Note this is a link to a specific spot on a much larger page that describes 
    the rest of the psycopg2 tools available to do other sorts of data type 
    converting/handling - may be usefull eventaully when dealing with date 
    types
    """
    if not np.isnan(float_or_nan):
        return PSYCOPG2_FLOAT(float_or_nan)
    
    return PSYCOPG2_NULL

psycopg2.extensions.register_adapter(float, float_handler_with_nan_to_null)

def na_to_null( float_or_nan ):
    """ Custom handler for pandas NAType """
    return psycopg2.extensions.AsIs('NULL')

psycopg2.extensions.register_adapter(pd._libs.missing.NAType, na_to_null)

