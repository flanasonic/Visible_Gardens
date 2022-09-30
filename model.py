from flask_sqlalchemy import SQLAlchemy

# create a SQLAlchemy object to represent our database - we'll call it "db"
db = SQLAlchemy()


#####################################################################
# Company
#####################################################################

class Company(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trade_name = db.Column(db.String(50))
    legal_name = db.Column(db.String(50))
    website = db.Column(db.String(50))
    country = db.Column(db.String(50))
    parent_id = db.Column(db.Integer)
    year_founded = db.Column(db.Integer)
    statement = db.Column(db.String(1000))
    total_employees = db.Column(db.Integer) #TODO: fix bug, not getting stored as Int
    legal_form = db.Column(db.String(50))
    for_profit = db.Column(db.Boolean, default=True)
    ownership = db.Column(db.String(50))
    business_focus = db.Column(db.String(75), default='specialty crop grower')
   

    # Company properties
    #  SQLAlchemy automatically fills these in with objects when querying
    #  ut when we create new Company object, we need to put in this info in
    # ourselvse. For example: new_company = db.Co....

    # a company has many products, a product has one company
    # a company has many facilities, a facility has one company
    products = db.relationship("Product", back_populates="company")
    facilities = db.relationship("Facility", back_populates="company")


    def __repr__(self):
        """Show info about company. """
        # these are inside db.Model
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )


#####################################################################
# Facility 

# a facility belongs to one company
# a facility needs to know the id of the company it belongs to
# a facility has an address

# with a many to one relationship, the 'many' side needs to know (store)
# the 'one' side's id 
# with one to one, we can just pick which side stores the other's id
#####################################################################

class Facility(db.Model):

    __tablename__ = 'facility'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer)
    address_id = db.Column(db.Integer)
    nickname = db.Column(db.String(75))
    type = db.Column(db.String(75))
    year_opened = db.Column(db.Integer)
    facility_employees = db.Column(db.Integer)

   # Declarative Table Configuration - SQLALchemy documentation: 
   # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['address_id'], ['address.id'], name='fk_facility_address'),
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['company_id'], ['company.id'], name='fk_facility_company')
            )

    # a facility has one address, an address has many facilities
    # a facility has one company, a company has many facilities
    address = db.relationship("Address", back_populates="facilities") 
    company = db.relationship("Company", back_populates="facilities")

    def __repr__(self):
        """Show info about facility."""
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )


#####################################################################
# Address
#####################################################################

class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_1 = db.Column(db.String(75))
    address_2 = db.Column(db.String(75))
    suite = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(10))
    postal = db.Column(db.String(10))
    country = db.Column(db.String(50))

    # an address Address properties/relationships
    facilities = db.relationship("Facility", back_populates="address")

    def __repr__(self):
        """Show info about address."""
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )


#####################################################################
# Product
#####################################################################

class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(50))
    user = db.Column(db.String(50), default='consumer')
    description = db.Column(db.String(1000))
    key_words = db.Column(db.String(1000))
    distribution = db.Column(db.String(50))

   # Declarative Table Configuration
   # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['company_id'], ['company.id'], name="fk_product_company"),
            )

    # Product properties/relationships
    # a product belongs to one compant
    company = db.relationship("Company", back_populates = "products")


    def __repr__(self):
        """Show info about product."""
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )
