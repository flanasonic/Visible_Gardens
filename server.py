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





@app.get("/")
def get_main_page():
    companies = Company.query.all()
    return render_template('main.html', companies=companies)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    




