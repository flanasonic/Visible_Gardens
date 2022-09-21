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
    year_founded = db.Column(db.Integer)
    country = db.Column(db.String(50))
    parent_id = db.Column(db.Integer)
    statement = db.Column(db.String(1000))
    total_employees = db.Column(db.Integer)
    legal_form = db.Column(db.String(50))
    for_profit = db.Column(db.Boolean, default=True)
    ownership = db.Column(db.String(50))
    business_focus = db.Column(db.String(75), default='specialty crop grower')
    address_id = db.Column(db.Integer)
   
   # Declarative Table Configuration
   # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['address_id'], ['address.id'], name="fk_product_address"),
    )

    # Company properties
    #   - SQLAlchemy will fill these in with objects when querying
    #   - We will populate these when "seeding" our database
    #   - We will populate these when inserting/updating a Company from our flask services
    address = db.relationship("Address")
    products = db.relationship("Product")
    facilities = db.relationship("Facility")

    def __repr__(self):
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
    zip = db.Column(db.String(10))
    country = db.Column(db.String(50))

    def __repr__(self):
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

    def __repr__(self):
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )

   # Declarative Table Configuration
   # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['company_id'], ['company.id'], name="fk_product_company"),
    )


#####################################################################
# Facility
#####################################################################

class Facility(db.Model):

    __tablename__ = 'facility'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer)
    nickname = db.Column(db.String(75))
    is_farm = db.Column(db.String(15))
    is_office = db.Column(db.String(15))
    is_country_hq = db.Column(db.String(15))
    is_other_type = db.Column(db.String(25))
    year_opened = db.Column(db.Integer)
    address_id = db.Column(db.Integer)
    facility_employees = db.Column(db.Integer)

   # Declarative Table Configuration - SQLALchemy documentation: 
   # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#declarative-table-configuration
    __table_args__ = (
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['address_id'], ['address.id'], name='fk_facility_address'),
        db.ForeignKeyConstraint(
            # local field   # foreign (table.column)
            ['company_id'], ['company.id'], name='fk_facility_company')    )

    # set up relationship between Facility and Address classes
    # a facility has one address, an address has many facilities
    address = db.relationship("Address")

    def __repr__(self):
        """Show info about facility."""

        return f'<Facility id={self.id} name={self.name}>'
