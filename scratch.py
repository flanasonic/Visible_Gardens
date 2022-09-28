from model import Company, Address, Product, Facility
from server import app

app.app_context().push()

##############################################
# RUN COMPANY QUERIES
##############################################

company_query_results = Company.query.all()

for company in company_query_results:
    print("    ---------------------------")
    print(company)

print("  ---------------------------")
# check_company_get = Company.query.get(7)
# print(check_company_get)

# check_company_filter_by = Company.query.filter_by(trade_name='Gotham Greens').all()
# print(check_company_filter_by)

# check_company_filter = Company.query.filter(Company.trade_name == 'Oishii').all()
# print(check_company_filter)

# check_company_filter_severalthings = Company.query.filter(Company.trade_name == 'Oishii', Company.product.user == 'consumer').all()
# print(check_company_filter_severalthings)




##############################################
# RUN PRODUCT QUERIES
##############################################

# check_product_all = Product.query.all()
# print(check_product_all)

# check_product_get = Product.query.get(7)
# print(check_product_get)

# check_product_count = Product.query.count()
# print(check_product_count)

# check_product_filter_by = Product.query.filter_by(name = 'Power Greens', user = 'consumer').all()
# print(check_product_filter_by)

# check_product_filter = Product.query.filter(Product.name == 'Power Greens').all()
# print(check_product_filter)

# check_product_filter_severalthings = Product.query.filter(Product.name == 'Power Greens', Product.user == 'consumer').all()
# print(check_product_filter_severalthings)




##############################################
# RUN FACILITY QUERIES
##############################################

# check_facility_all = Facility.query.all()
# print(check_facility_all)


##############################################
# CREATE SOME TEST RECORDS! 

# -- create a 'new_company' test object
# new_company = Company(trade_name = 'Bowery Farms', website = 'www.boweryfarming.com', year_founded = 2018, country = 'US', state_incorporated = 'NY', summary = 'We grow really good salad greens', total_employees = 300, legal_form = 'LLC', for_profit = True)

# Company(trade_name = 'Gotham Greens', website = 'www.gothamgreens.com', year_founded = 2016, country = 'US', state_incorporated = 'NY', summary = 'Fresh locally grown greens, vegetables, and fruits', total_employees = 600, legal_form = 'LLC', for_profit = True)


# -- create a 'new_product' test object
# new_product = Product(name = "Spicy blend", category = "microgreens", user= 'consumer', description = "a mix of spicy microgreens")
# new_product = Product(name = "Omakase berry", category = "berries", user= 'consumer', description = "the best strawberries in the world")


# -- create a 'new_address' test object
# new_address = Address(company_id=1, address_type = 'facility', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')
# new_address = Address(=2, address_type = 'facility', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')
# new_address = Address(company_id=1, address_type = 'legal', address_1 = '100 Main Street', city = 'Brooklyn', state ='NY', zip = 11215, country= 'US')

# -- create a 'new_facility' test object
# new_facility = Facility(company_id=1, name='Sunset Park', type='farm', output='berries', yr_opened=2022, address_id=2)
    