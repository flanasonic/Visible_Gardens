from model import db, Company
from flask import Flask, render_template, request, jsonify
from sqlalchemy import literal
from search import search_product


DB_URI = 'postgresql:///indoorfarms'
# TODO: make a config for database URI

# create a Flask object and call it "app"
app = Flask(__name__)

# tell our app where to find the db
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
# print our SQL commands to Python terminal, shut off if needed
app.config["SQLALCHEMY_ECHO"] = True
# include this line and set to False, otherwise it will waste memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# let's 'glue' our Flask app ('app') to our Flask SQLAlchemy object ('db') 
# and tell the app to start running with db
db.init_app(app)


# Below are our view functions, view functions return a string 
# (usually a string of HTML)
# "Routes" are declared using "decorators" - they indicate which URL(s) will
# run each view function
# The "get" method is implied by default in an HTML form


@app.get("/")
def get_main():
    return render_template('home.html')

# This function gets called by our search form and will show search results
# Our queries are in 'search.py', we call them on this page
@app.get("/search.json")
def get_results():
    words = request.args['search'] 
    results = search_product(words) # function defined in search.py
    return jsonify(results)


# This gets called by our search form and will show search results
# @app.get("/search")
# def get_search_results():
#     search_word = request.args['search']
#     companies = Company.query.filter(Company.trade_name
#                                      .contains(literal(search_word))
#                                      ).all()
#     print(companies)
#     return render_template('results.html', companies=companies)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
