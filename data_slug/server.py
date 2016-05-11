#!/usr/bin/env python3
from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth

from server_modules import core
from server_modules import users

__LOCAL = True
__PORT = 5050
__DEBUG = True


def get_app(debug=False):

    app = Flask("Data Slug Server")
    app.debug = debug
    app.auth = HTTPBasicAuth()

    core.set_database_connector(app)
    users.set_password_validification(app)

    core.register_routes(app)
    users.register_routes(app)

    return app

if __name__ == "__main__":

    app = get_app(debug=__DEBUG)
    app.run(host="127.0.0.1" if __LOCAL else "0.0.0.0", port=__PORT)
