from model import db, Company
from flask import Flask, render_template, request, jsonify
from sqlalchemy import literal


DB_URI = 'postgresql:///indoorfarms'
# TODO: make a config for database URI

# create a Flask object and call it "app"
app = Flask(__name__)

# tell our app where to find the db
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
# print our SQL commands to Python terminal, shut off if needed
app.config["SQLALCHEMY_ECHO"] = False
# include this line and set to False, otherwise it will waste memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# let's 'glue' our Flask app (named 'app') to our Flask SQLAlchemy object (named 'db') and tell the app to start running with db
db.init_app(app)


# Views are functions that return a string (usually HTML)
# Routes define the URL that will run a view function.
# They are declared by using decorators.
# the GET method is implied by default in an HTML form

@app.get("/")
def get_main():
    return render_template('home.html')

# This gets called by our search form and will
# show search results
@app.get("/search.json")
def get_results():
    search_word = request.args['search'] 
    companies = Company.query.filter(Company.trade_name
                                     .contains(literal(search_word))
                                     ).all()
    result = []
    for co in companies:
        co_json = {
            "id": co.id,
            "trade_name": co.trade_name,
            "country": co.country            
        }
        result.append(co_json)
    return jsonify(result)


# This gets called by our search form and will
# show search results
@app.get("/search")
def get_search_results():
    search_word = request.args['search']
    companies = Company.query.filter(Company.trade_name
                                     .contains(literal(search_word))
                                     ).all()
    print(companies)
    return render_template('results.html', companies=companies)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
