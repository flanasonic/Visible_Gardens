**********
initdb.py 
**********

Start here. 



Some helpful functions created to get the database up and running with current data.

1. arg_parser 
This uses the argparse module's ArugmentParser class to enable us to add 
command line arguments to our program. This lets use save time on repetitive
things like downloading the most recent version of our data from our google sheets 
file. It saves the current version locally in our /data directory as a CSV,
and puts the previous version in the /data/backup directory.

To download all of our sheets from google sheets:
$ python ./initdb.py -update all sheets

To download a specific sheet by name:
$ python ./initdb.py -update [sheet name]

*************************
db_utils/__init__.py
*************************

def download_google_worksheet

def backup_data_file


def get_matching_column_names
 
 Function looks at columns in our spreadsheet vs. our table and finds the 
 intersection, filtering out any spreadsheet columns that don't belong in 
 the table.

 def float_handler_with_nan_to_null


 def na_to_null
