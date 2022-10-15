from model import Company, Address, Product, Facility
from sqlalchemy.sql.expression import literal


# search companies by product name
"""


"""

# Write a function that takes in a search term and searches the 
# 'name' column in the Product table column for matches 
# When it finds matches, it gets a bunch of data related to each
# matched product (e.g. the company) and makes a dict of some fields
# we want to see on the search results part of our web page.  We'll add
# dicts like this for each product our search terms match.
#
# We'll call this function from our flask route "/search.json" and 
# return it our list of dicts.  
# Our flask route will turn the list of dicts it gets back from this function
# into json and send it back whenever a user performs a search - and makes the 
# ajax/fetch thing GET from our "/search.json" route
#
# Note the names of the keys to each dict we put into the list here, we'll 
# use these same key names in any React components that render our search 
# results.
def search_product(search_terms: str):
    print(f"searching for {search_terms}")
    results = []
    word_list = search_terms.split(" ")
    # loop over the words the user is searching for and
    # query the database with each one
    for word in word_list:
        # query the name column of our Product table to see
        # if it contains this word
        products = Product.query.filter(Product.name
                                        .contains(literal(word)
                                        )).all()

        # hopefully we got some products that matched our search word
        # let's loop over the results for this word and add some data 
        # from the product object (and other objects related to it like 
        # company)
        for product in products:
            # let's get the company for this product using the company
            # relationship on our Product object
            # let's also get the default address for this company using
            # the address relationship on our Company object
            company = product.company
            address = company.address
        
            # let's make an object with some data we want to send back to our
            # web app - we'll use these in our react props
            this_result = {
                "product": product.to_dict(),
                "company": company.to_dict()
            }
            this_result["company"].update({ "address": address.to_dict() })
            facilities = company.facilities
            this_result["facilities"] = []
            for facility in facilities:
                this_facility = facility.to_dict()
                this_facility.update({ "address": facility.address.to_dict() })
                this_result["facilities"].append(this_facility)                
            results.append(this_result)
    return results





