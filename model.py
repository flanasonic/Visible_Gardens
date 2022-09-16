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
    app.config["SQLALCHEMY_ECHO"] = False
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

    __tablename__ = 'company'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    trade_name = db.Column(db.String(50), nullable=False)
    legal_name = db.Column(db.String(50))
    website = db.Column(db.String(50))
    year_founded = db.Column(db.Integer)
    country = db.Column(db.String(25), nullable=False)
    state_incorporated = db.Column(db.String(2))
    parent_company_id = db.Column(db.Integer)
    child_company_id = db.Column(db.Integer)
    legal_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    marketing_statement = db.Column(db.String(500))
    total_employees = db.Column(db.Integer)
    legal_form = db.Column(db.String(50))
    for_profit = db.Column(db.Boolean, default=True)
    ownership = db.Column(db.String(50))
    business_focus = db.Column(db.String(75), default='specialty crop grower',)
    # back_populates tells our sql model that if something changes in this model, it should change 
    # that attribute in the other model


    # set up SQLAlchemy relationship between company and product classes
    # a company has many products, a product has only one company
    products = db.relationship("Product", back_populates="company")

    # set up relationship between company and address classes
    # an address has one company, a company has many addresses
    addresses = db.relationship("Address", back_populates="company")

    # set up relationship between company and facility classes
    # a company has many facilities, a facility has only one company
    facilities = db.relationship("Facility", back_populates="company")

    # so...we want to be able to call:
    #   company.products and get all of the products associated with that company
    #   company.addresses and get all of the addresses associated with that company
    #   company.facilities and get all of the facilities associated with that company
    #   ...and also...
    #   product.company and get the company associated with that product
    #   address.company and get the company associated with that address
    #   facility.company and get the company associated with that facility
    

    def __repr__(self):
        """Show info about company."""

        return f'<Company id={self.id} name={self.trade_name}>'




class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    user = db.Column(db.String(50), default='consumer')
    description = db.Column(db.String(300))
    key_words = db.Column(db.String(300))
    distribution = db.Column(db.String(50))
    
    # set up relationship between company and product classes
    # a company has many products, a product has one company
    company = db.relationship("Company", back_populates="products")

    # so, we want to be able to call:
    #   product.company and get the company associated with that product
    #   company.products and get all of the products associated with that company



    def __repr__(self):
        """Show info about product."""

        return f'<Product id={self.id} name={self.name}>'



class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    address_type = db.Column(db.String(50), nullable=False)
    address_1 = db.Column(db.String(50), nullable=False)
    address_2 = db.Column(db.String(50))
    suite = db.Column(db.String(25))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    country= db.Column(db.String(50))
    
    def __repr__(self):
        """Show info about cat."""

        return f'<Address id={self.id} name={self.company_id}>'

    # set up relationship between address and facility classes
    # an address has many facilities, a facility has one address  
    company = db.relationship("Company", back_populates="addresses")

    # set up relationship between address and company classes
    # an address has one company, a company has many address  
    facilities = db.relationship("Facility", back_populates="address")

    # so, we want to be able to call:
    #   address.company and get the company associated with that address
    #   company.addresses and get all addresses associated with that company
    #   address.facilities and get all facilities associated with that address
    #   facility.address and get the address associated with that facility



class Facility(db.Model):

    __tablename__ = 'facility'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    output = db.Column(db.String(50))
    year_opened = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    employees = db.Column(db.Integer)
    
    def __repr__(self):
        """Show info about facility."""

        return f'<Facility id={self.id} name={self.name}>'

    # set up relationship between facility and company classes
    # a facility has one company, a company has many facilities
    company = db.relationship("Company", back_populates="facilities")

    # set up relationship between facility and address classes
    # a facility has one address, an address has many facilities
    address = db.relationship("Address", back_populates="facilities")

    # so, we want to be able to call:
    #   facility.company and get the company associated with that facility
    #   company.facilities and get all facilities associated with that company
    #   facility.address and get the address associates with that facility
        #   address.facilities and get all facilities associated with that address




###########################

# if __name__ == "__main__" is like saying "When you ran Python, if this 
# script we're in now is the one you told Oython to run, then name will be 
# equal to "__main__" 
# (as opposed to running another script and just importing this one)


if __name__ == "__main__":
    from server import app # this line imports our Flask app

    # now call function connect_to_db() to connect our Flask app (called 'app')
    # to our database called 'indoorfarms' 
    db_name = 'indoorfarms'
    connect_to_db(app, db_name)



###########################

## now, let's create the tables using the db connection we established above
## we only need to do this once 
## then again any time we need to recreate our tables (like if we make a 
## change in model.py that requires changing a table's schema)
db.create_all()



###########################


## CREATE SOME TEST RECORDS! 


## USE db.session! 
# db.session.add(new_company)
# db.session.add(new_product)
# db.session.add(new_facility)

## we use db.session for database transactions
## it lets us store the modifications we plan to make to our db
## the changes don't actually get made until we commit
## we only have to use db.session.add() to add a new object once — 
## we don’t need to keep adding it to the session each time we change it



## COMMIT THE CHANGES!
# db.session.commit()