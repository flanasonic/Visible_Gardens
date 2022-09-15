from flask_sqlalchemy import SQLAlchemy

# create a SQLAlchemy object to represent our database - we'll call it "db"
db = SQLAlchemy()

# create a function called "connect_to_db" to connect our db to our Flask app
# pass in:
# 1) the name of our Flask app, which is 'app' 
# 2) the name of our database
def connect_to_db(app, db_name):
    # print(flask_app)

    # tells our app where to find the db
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql:///{db_name}'
    # prints our SQL commands to Python terminal, can shut off when needed
    app.config["SQLALCHEMY_ECHO"] = True 
    # need to include this line -set to False, otherwise it will waste memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    # let's 'glue' our Flask app (named 'app') to our 
    # Flask SQLAlchemy object (named 'db')
    db.app = app
    # and tell the app to start running with db
    db.init_app(app)


###########################

# now let's create our classes
# db.Model is a superclass, Company is a subclass of db.Model
# We say "all models should subclass db.Model", meaning all of the 
# models/classes we create here are subclasses of db.Model
# It's like saying "take everything in db.Model and let me layer 
# this other stuff on top"

class Company(db.Model):

    __tablename__ = 'companies'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    trade_name = db.Column(db.String(50), nullable=False)
    legal_name = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(50), nullable=True)
    founded = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(25), nullable=False)
    state_incorporated = db.Column(db.String(2), nullable=True)
    parent_company_id = db.Column(db.Integer, nullable=True)
    child_company_id = db.Column(db.Integer, nullable=True)
    legal_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    summary = db.Column(db.String(500), nullable=True)
    total_employees = db.Column(db.Integer, nullable=True)
    legal_form = db.Column(db.String(50), nullable=True,)
    for_profit = db.Column(db.Boolean, default=True, nullable=True,)
    business_focus = db.Column(db.String(75), nullable=True, default='specialty crop grower',)

# use db.relationship to set up SQLAlchemy relationships between companies and products tables
# back_populates tells our sql model that if something changes in this model, it should change 
# that attribute in the other model
# not sure if this is correctly set up...   
# one company has many products, but a product has only one company
# so, we want to be able to call products.company ?????
# (and also be able to call company.products) ?????
   
    products = db.relationship("Product", back_populates="company")

    def __repr__(self):
        """Show info about company."""

        return f'<Company id={self.id} name={self.trade_name}>'




class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    user = db.Column(db.String(50), nullable=True, default='consumer')
    distribution = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(300), nullable=True)
    key_words = db.Column(db.String(300), nullable=True)
    
    # set up relationship between companies and products tables
    # not sure if this is correctly set up...   
    # one company has many products, a product can only have one company
    # so, we want to be able to call company.products????
    # (and also be able to call products.company)????
    company = db.relationship("Company", back_populates="products")


    def __repr__(self):
        """Show info about product."""

        return f'<Product id={self.id} name={self.name}>'




class Facility(db.Model):

    __tablename__ = 'facilities'

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True, )
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    output = db.Column(db.String(50), nullable=True)
    opened = db.Column(db.Integer, nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    key_words = db.Column(db.String(300), nullable=True)
    
    def __repr__(self):
        """Show info about facility."""

        return f'<Facility id={self.id} name={self.name}>'




class Address(db.Model):

    __tablename__ = 'addresses'

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True, )
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    address_1 = db.Column(db.String(50), nullable=False)
    address_2 = db.Column(db.String(50), nullable=True)
    suite = db.Column(db.String(25), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    country= db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        """Show info about cat."""

        return f'<Facility id={self.id} name={self.name}>'



###########################

# if __name__ == "__main__" is like saying "When you ran Python, if this 
# script we're in now is the one you told python to run, then name will be 
# equal to "__main__" 
# (This is as opposed to running another script and just importing this one)


if __name__ == "__main__":
    from server import app # this line imports our Flask app

    # now call function connect_to_db() to connect our Flask app (called 'app')
    # to our database called 'indoorfarms' 

    db_name = 'indoorfarms'
    connect_to_db(app, db_name)



###########################

    # now, let's create the tables usind the db connection we established above
    # we only need to do this once 
    # then again any time we need to recreate our tables (like if we make a 
    # change in model.py that requires changing a table's schema)
    # db.create_all()



###########################


    ## CREATE SOME TEST RECORDS! 

    ## create a 'company' test object
    # company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    # name = db.Column(db.String(50), nullable=False)
    # category = db.Column(db.String(50), nullable=True)
    # user = db.Column(db.String(50), nullable=True, default='consumer')
    # distribution = db.Column(db.String(50), nullable=True)
    # description = db.Column(db.String(300), nullable=True)
    # key_words = db.Column(db.String(300), nullable=True)
    # print(new_company)


    ## USE db.session! 

    ## we use db.session for database transactions
    ## it lets us store the modifications we plan to make to our db
    ## the changes don't actually get made until we commit
    ## we only have to use db.session.add() to add a new object once — 
    ## we don’t need to keep adding it to the session each time we change it
    # db.session.add(new_company)


    ## COMMIT THE CHANGES!

    # db.session.commit()


    ## RUN SOME QUERIES!

    # check_company_all = Company.query.all()
    # print(check_company_all)

    # check_company_get = Company.query.get(1)
    # print(check_company_get)
    
    # check_company_filter_by = Company.query.filter_by(name='Gotham Greens').all()
    # print(check_company_filter_by)

    # check_company_filter = Company.query.filter(Company.name == 'Oishii').all()
    # print(check_company_filter)

    # check_company_filter_severalthings = Company.query.filter(Company.name == 'Oishii'. Company.user == 'consumer').all()
    # print(check_company_filter_severalthings)


###########################

    ## FOR REFERENCE: Query Execution Methods/ Fetching Records

    # .get()  
    ## Get a record by its primary key

    # .all() 
    ## Get all records as a list

    # .first() 
    ## Get first record or 'None'

    # .one() 
    ## Get first record, error if 0 or more than 1

    # .count()
    ## Get number of records found without fetching



###########################

    ## FOR REFERENCE: More Flexible Querying

    ## simple version: 
    # Employee.query.filter_by(name='Liz')
    # Employee.query.filter(Employee.name == 'Liz')

    ## more flexible version:
    # db.session.query(Employee).filter_by(name='Liz')
    # db.session.query(Employee).filter(Employee.name == 'Liz')

###########################

    ## FOR REFERENCE: Get by PK
#     >>> Department.query.filter_by(dept_code='fin').one()
# <Department code=fin name=Finance>
# >>> Department.query.get('fin')
# <Department code=fin name=Finance>

