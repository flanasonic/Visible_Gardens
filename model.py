from tkinter.tix import INTEGER
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):

    __tablename__ = 'companies'

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True, )
    trade_name = db.Column(db.String(50), nullable=False)
    legal_name = db.Column(db.String(50))
    website = db.Column(db.String(50))
    founded = db.Column(db.Integer)
    country = db.Column(db.String(25))
    state_inc = db.Column(db.String(2))
    parent_company_id = db.Column(db.Integer)
    child_company_id = db.Column(db.Integer)
    legal_address_id = db.Column(db.Integer)
    summary = db.Column(db.String(500))
    total_employees = db.Column(db.Integer)
    legal_form = db.Column(db.String(50))
    for_profit = db.Column(db.Boolean(default=True))
    business_focus = db.Column(db.String(75), nullable=False, default='specialty crop grower',)


    def __repr__(self):
        """Show info about cat."""

        return f'<Company id={self.id} name={self.trade_name}'


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True, )
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    user = db.Column(db.String(50))
    distribution = db.Column(db.String(50))
    description = db.Column(db.String(300))
    key_words = db.Column(db.String(300))
    


    def __repr__(self):
        """Show info about cat."""

        return f'<Product id={self.id} name={self.name}'


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
        """Show info about cat."""

        return f'<Facility id={self.id} name={self.name}'

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

        return f'<Facility id={self.id} name={self.name}'