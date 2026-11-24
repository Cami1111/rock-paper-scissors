# this is the "web_app/__init__.py" file...
# it acts as the entry point for the web_app directory
# later when we tell flask to go run an app that has been defined
# in the web_app directory, it's going to look here first
# and execute this code to run the app in our browser

import os
from dotenv import load_dotenv

from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.rps_routes import rps_routes
from web_app.routes.stocks_routes import stocks_routes

load_dotenv()

# used by flask to securely send flash messages
SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")  # set this to something else on production!!!


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(home_routes)
    app.register_blueprint(rps_routes)
    app.register_blueprint(stocks_routes)
    return app


if __name__ == "__main__":
    # when you run this from the command line, the following code
    # will be executed
    my_app = create_app()
    my_app.run(debug=True)
