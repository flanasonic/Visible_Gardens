"""Server for movie ratings app."""

from flask import Flask

# create a Flask object and call it "app" 
# TODO: ?? create a Flask object called "app" - does it represent our server
app = Flask(__name__)


# Replace this with routes and view functions!


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)
