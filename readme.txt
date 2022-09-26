**********
initdb.py 
**********

Start here. This file contains contains some helpful functions to get our
database up and running with current data.

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


2. 



db_utils > __init__.py
