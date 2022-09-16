# this script removes any existing tables from the database and recreates them
# 1) drops all tables 
# 2) creates all tables - based on table name, columns as defined in model 
# objects in model.py
# 3) loads data from csv files into tables

# now we have a fresh database!

from model import Company, Product, Address, Facility
from model import db
from sqlalchemy import Session, create_engine
from server import DB_URI
# TODO: get DB_URI from a config

