from model import db, Company
from flask import Flask, render_template



DB_URI = 'postgresql:///indoorfarms'
# TODO: make a config for database URI

# create a Flask object and call it "app" 
app = Flask(__name__)

# tells our app where to find the db
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
# prints our SQL commands to Python terminal, can shut off when needed
app.config["SQLALCHEMY_ECHO"] = False
# need to include this line -set to False, otherwise it will waste memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# let's 'glue' our Flask app (named 'app') to our 
# Flask SQLAlchemy object (named 'db')
# and tell the app to start running with db
db.init_app(app)



# Views are functions that return a string (usually HTML)
# Routes define the URL that will run a view function. 
# They are declared by using decorators.
# @app.route("/")
# the GET method is implied by default in an HTML form
#  @app.get("/")
def get_main_page():
    return render_template('main.html')


@app.get("/search")
def get_search_form():
    # companies = Company.query.all()
    return render_template('/search.html')

# @app.get("/results")
# def get_search_results():
#     companies = Company.query.all()
#     return render_template('main.html', companies=companies)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    




