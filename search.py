from model import Company, Address, Product, Facility



# search companies by product name
"""


"""





# write a function that takes in a search term and searches the
# product table for matches, looking in columns in this order:
#  'name', 'category', 'key_words"
# when it finds a match, it takes the company puts in a list
# returns the list of companies that match the key words

def search_product_get_company(search_terms):
    results = []
    word_list = search_terms.split(" ")
    for word in word_list:
        products = Product.query.filter(Product.name.ilike(word)).all()
        results = results + [product.company for product in products]
        print([product.company for product in products])
    return results





