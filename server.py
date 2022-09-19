"""Server for movie ratings app."""

from flask import Flask

DB_URI = 'postgresql:///indoorfarms'
# TODO: make a config for database URI

# create a Flask object and call it "app" 
app = Flask(__name__)


# Replace this with routes and view functions!


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)

    # now call function connect_to_db() to connect our Flask app (called 'app')
    # to our database called 'indoorfarms' 
    
    # tells our app where to find the db
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    # prints our SQL commands to Python terminal, can shut off when needed
    app.config["SQLALCHEMY_ECHO"] = False
    # need to include this line -set to False, otherwise it will waste memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 


    # let's 'glue' our Flask app (named 'app') to our 
    # Flask SQLAlchemy object (named 'db')
    # and tell the app to start running with db
    from model import db
    db.init_app(app)



