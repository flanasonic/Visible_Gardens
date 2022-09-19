from flask_sqlalchemy import SQLAlchemy

# create a SQLAlchemy object to represent our database - we'll call it "db"
db = SQLAlchemy()


###########################

# now let's create our classes
# db.Model is a superclass, Company is a subclass of db.Model
class Company(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trade_name = db.Column(db.String(50), nullable=False)
    legal_name = db.Column(db.String(50))
    website = db.Column(db.String(50))
    year_founded = db.Column(db.Integer)
    country = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer)
    statement = db.Column(db.String(1000))
    total_employees = db.Column(db.Integer)
    legal_form = db.Column(db.String(50))
    for_profit = db.Column(db.Boolean, default=True)
    ownership = db.Column(db.String(50))
    business_focus = db.Column(db.String(75), default='specialty crop grower',)
   

    # set up SQLAlchemy relationship between Company and Product classes
    # a company has many products, a product has only one company
    # back_populates tells our sql model that if something changes in this model, 
    # it should changethat attribute in the other model
    # products = db.relationship("Product", back_populates="company")

    # set up relationship between Company and Address classes
    # an address has one company, a company has many addresses
    # legal_address = db.relationship("Address")
    # legal_address = db.relationship("Address", back_populates="company")

    # set up relationship between Company and Facility classes
    # a company has many facilities, a facility has only one company
    # facilities = db.relationship("Facility")
    # facilities = db.relationship("Facility", back_populates="company")

    # so...we want to be able to call:
    #   company.products and get all of the products associated with that company
    #   company.addresses and get all of the addresses associated with that company
    #   company.facilities and get all of the facilities associated with that company
    #   ...and also...
    #   product.company and get the company associated with that product
    #   address.company and get the company associated with that address
    #   facility.company and get the company associated with that facility

    def __repr__(self):
        return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )


# class Product(db.Model):

#     __tablename__ = 'product'

#     id = db.Column(db.Integer, primary_key=True autoincrement=True)
#     # TODO: do we need 'references company' for company_id?
#     company_id = db.Column(db.Integer)
#     name = db.Column(db.String(), nullable=False)
#     category = db.Column(db.String(50))
#     user = db.Column(db.String(50), default='consumer')
#     description = db.Column(db.String(1000))
#     key_words = db.Column(db.String(1000))
#     distribution = db.Column(db.String(50))

#     __table_args__ = (
#         db.ForeignKeyConstraint(
#             ['company_id'], ['company.id'], name="fk_product_company"),
#     )

    # set up relationship between Product and Company classes
    # a product has one company, a company has many products
    # company = db.relationship("Company", back_populates="products")

    # so, we want to be able to call:
    #   product.company and get the company associated with that product
    #   company.products and get all of the products associated with that company

    # def __repr__(self):
    #     return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )


# class Address(db.Model):

#     __tablename__ = 'address'

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
#     address_type = db.Column(db.String(75), nullable=False)
#     address_1 = db.Column(db.String(75), nullable=False)
#     address_2 = db.Column(db.String(75))
#     suite = db.Column(db.String(50))
#     city = db.Column(db.String(50), nullable=False)
#     state = db.Column(db.String(10), nullable=False)
#     zip = db.Column(db.String(10), nullable=False)
#     country = db.Column(db.String(50))

#     def __repr__(self):
#         return " ".join( [f"({name}: {getattr(self, name)})" for name in self.__table__.columns.keys()] )

    # set up relationship between Address and Company classes
    # an address has one company, a company has many addresses?
    # company = db.relationship("Company", back_populates="addresses")

    # set up relationship between Address and Facility classes
    # an address has many facilities, a facility has one address
    # facilities = db.relationship("Facility", back_populates="address")

    # so, we want to be able to call:
    #   address.company and get the company associated with that address
    #   company.addresses and get all addresses associated with that company
    #   address.facilities and get all facilities associated with that address
    #   facility.address and get the address associated with that facility


# class Facility(db.Model):

#     __tablename__ = 'facility'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     company_id = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String(50))
#     type = db.Column(db.String(50))
#     output = db.Column(db.String(50))
#     year_opened = db.Column(db.Integer)
#     address_id = db.Column(db.Integer)
#     employees = db.Column(db.Integer)

    # __table_args__ = (
    #     db.ForeignKeyConstraint(
    #         ['company_id'], ['company.id'], name='fk_facility_company'),
    #     db.ForeignKeyConstraint(
    #         ['address_id'], ['address.id'], name='fk_facility_address')
    # )

    # def __repr__(self):
    #     """Show info about facility."""

    #     return f'<Facility id={self.id} name={self.name}>'

    # set up relationship between Facility and Company classes
    # a facility has one company, a company has many facilities
    # company = db.relationship("Company", back_populates="facilities")

    # set up relationship between Facility and Address classes
    # a facility has one address, an address has many facilities
    # address = db.relationship("Address", back_populates="facilities")

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


###########################

# now, let's create the tables using the db connection we established above
# we only need to do this once
# then again any time we need to recreate our tables (like if we make a
# change in model.py that requires changing a table's schema)
# db.create_all()


###########################


# CREATE SOME TEST RECORDS!


# USE db.session!
# db.session.add(new_company)
# db.session.add(new_product)
# db.session.add(new_facility)

# we use db.session for database transactions
# it lets us store the modifications we plan to make to our db
# the changes don't actually get made until we commit
# we only have to use db.session.add() to add a new object once —
# we don’t need to keep adding it to the session each time we change it


# COMMIT THE CHANGES!
# db.session.commit()
