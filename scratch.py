from model import Company, Address, Product, Facility
from server import app
# from sqlalchemy.orm import Session #TODO: ok to add this??
# from sqlalchemy import create_engine #TODO: ok to add this??


app.app_context().push()



##############################################
# COMPANY QUERIES
##############################################

### using .get() to search by primary key ###

## fetch company record by primary key
# company_get_by_id = Company.query.get(7)
# print("  ---------------------------")
# print(company_get_by_id)
# print("  ---------------------------")


### firing the select with .all() ###

# ## fetch all company records
# companies = Company.query.all()
# for company in companies:
#     print("    ---------------------------")
#     print(company)
# print("  ---------------------------")


### firing the select with .first() ###

# ## fetch first company
# company = Company.query.first()
# print("    ---------------------------")
# print(company)
# print("  ---------------------------")


##############################################
# ADDRESS QUERIES
##############################################

# ##fetch all address records
# addresses = Address.query.all()
# for address in addresses:
#     print("    ---------------------------")
#     print(address)
# print("  ---------------------------")


##############################################
### FILTERING....###
##############################################

### using .filter_by() ###

# company_results = Company.query.filter_by(trade_name = "Gotham Greens").all()
# print("  ---------------------------")
# print(company_filter_by)
# print("  ---------------------------")


### using .filter() ###

# companies = Company.query.filter(Company.trade_name == "Gotham Greens").all()
# for company in companies:
#     print("  ---------------------------")
#     print(company.products)
#     print("  ---------------------------")


# companies = Company.query.join(Product).filter(
#     (Company.trade_name == "Oishii")
#     & (Product.user == "consumer")
#     ).all()
# for company in companies:
#     print("  ---------------------------")
#     print(company.products)
#     print("  ---------------------------")



# facilities = Facility.query.all()
# for facility in facilities:
#     print(facility.address)

# companies = Company.query.join(Product).filter(
#     (Company.trade_name == "Oishii")
#     & (Product.user == "consumer")
#     ).all()
# for company in companies:
#     print("  ---------------------------")
#     print(company.products)
#     print("  ---------------------------")


# address_facilities = Address.query.all()
# for address in address_facilities:
#     print(address.facilities)


# companies = Company.query.join(Product).filter(
# (Company.trade_name == "Oishii") & 
# (Product.user == "consumer")).all()
# for company in companies:
#     print("  ---------------------------")
#     print(company.products)
#     print("  ---------------------------")



### filter using .endswith() ###
# complex_query = Company.query.filter(Company.trade_name.endswith('s')).all()
# print(complex_query)


### order_by ###
# company_query_ordered = Company.query.order_by(Company.trade_name).all()
# for company in company_query_ordered:
#     print("    ---------------------------")
#     print(company)
# print("  ---------------------------")


# products_by_company = Product.query.filter_by(company_trade_name = "Gotham Greens").all()
# print(products_by_company)



##############################################
# RUN PRODUCT QUERIES
##############################################


# check_product_get = Product.query.get(7)
# print(check_product_get)

# check_product_count = Product.query.count()
# print(check_product_count)

# check_product_filter_by = Product.query.filter_by(name = 'Power Greens', user = 'consumer').all()
# print(check_product_filter_by)

# check_product_filter = Product.query.filter(Product.name == 'Power Greens').all()
# print(check_product_filter)





## fetch all product records
# products = Product.query.all()
# for product in products:
#     print("    ---------------------------")
#     print(product)
# print("  ---------------------------")



##############################################
# RUN FACILITY QUERIES
##############################################

# check_facility_all = Facility.query.all()
# print(check_facility_all)


##############################################
# CREATE SOME TEST RECORDS! 
##############################################

## create a 'new_company' test object
# new_company = Company(trade_name = 'Bowery Farms', website = 'www.boweryfarming.com', year_founded = 2018, country = 'US', state_incorporated = 'NY', summary = 'We grow really good salad greens', total_employees = 300, legal_form = 'LLC', for_profit = True)

# Company(trade_name = 'Gotham Greens', website = 'www.gothamgreens.com', year_founded = 2016, country = 'US', state_incorporated = 'NY', summary = 'Fresh locally grown greens, vegetables, and fruits', total_employees = 600, legal_form = 'LLC', for_profit = True)


## create a 'new_product' test object
# new_product = Product(name = "Spicy blend", category = "microgreens", user= 'consumer', description = "a mix of spicy microgreens")
# new_product = Product(name = "Omakase berry", category = "berries", user= 'consumer', description = "the best strawberries in the world")


## reate a 'new_address' test object
# new_address = Address(company_id=1, address_type = 'facility', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')
# new_address = Address(=2, address_type = 'facility', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')
# new_address = Address(company_id=1, address_type = 'legal', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')

## create a 'new_facility' test object
# new_facility = Facility(company_id=1, name='Sunset Park', type='farm', output='berries', yr_opened=2022, address_id=2)
    


##############################################
## GOOD QUERIES
##############################################

## fetch company records, filter by:
## Company.trade_name & Product.user
# companies = Company.query.join(Product).filter(
#     (Company.trade_name == "Farm.One")
#     & (Product.user == "consumer")
#     ).all()
# for company in companies:
#     print("  ---------------------------")
#     print(company.products)
#     print("  ---------------------------")
 
 
# company_results = Company.query.filter_by(trade_name = "Gotham Greens").all()
# print(company_results)



## write a query to search for companies with facilities of type "farm" located 
## in a given city & state and get a list of the products they offer
# facilities = Facility.query.join(Address).filter(Facility.type == "farm", Address.state == "NY", ).all()
# for facility in facilities:
#     print("  ---------------------------")
#     print(f"Company: {facility.company.trade_name}")
#     print(f"Farm(s) located in: {facility.address.city}, {facility.address.state}")
#     print("Products: ")
#     for product in facility.company.products:
#         print(f"{product.name},")
#     print("  ---------------------------")


# write a query to search for a given company and get a list of its facilities
# with the type and location (city, state) of each
# TODO: Group lists by faciltiy type
# companies = Company.query.join(Facility).filter(Company.trade_name == "Gotham Greens").all()
# for company in companies:
#     print(f"{company.trade_name} has the following facilities: ")
#     for facility in company.facilities:
#         print(f"A {facility.type} in {facility.address.city}, {facility.address.state}")
# #     print(f"{target_co} has the following facilities: ")
#     for facility in company.facilities:
#         print(f" A {facility.type} in {facility.address.city}, {facility.address.state}.")
# # for company in company_facilities:
#     print(Company.facility)
# # print(f"{target_co} has the following facilities: ")
# for company in company_facilities:
#     print(f"{company.facility.type}")
#     print("  ---------------------------")



# # fetch all address records, filter by state,
# # and print their facilities
# addresses = Address.query.filter_by(state = "NJ").all()
# for address in addresses:
#     print(address)


# find all companies with facilities in state NY 
## fetch company records, filter by:
## ...
# companies = Company.query.join(Facility, Address).filter(Address.facilities.state == "NY").all()
# for company in companies:
#     print("  ---------------------------")
#     print(company)
#     print("  ---------------------------")
 


## write a search to find companies with facilities in NY state growing "greens"
# Company: 
# get cols: trade_name, website, year_founded, statement
# Facility: 
# get cols: type, address
# filter by: address.state = "NY"
# Products: 
# get cols: name, category, description
# filter by: keyword = "greens"

# join facility and address tables
# filter by address state==NJ
# for each faciliy, print its address
# facilities = Facility.query.join(Address, Product).all()
# facilities = Facility.query.join(Address).join(Product)
# facilities = facilities.join(Product)
# facilities_product = facilities.filter(Address.state == "NY").all()
# for facility in facilities:
#     print(facility.address.city)

# companies = db.session.query(Company).all()
# print(companies)


