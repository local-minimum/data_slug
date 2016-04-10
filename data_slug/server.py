#!/usr/bin/env python3
from flask import Flask
from server_modules import project_setup

__LOCAL = True
__PORT = 5000
__DEBUG = True


def get_app(debug=False):

    app = Flask("Data Slug Server")
    app.debug = debug
    return app

if __name__ == "__main__":

    app = get_app(debug=__DEBUG)

    project_setup(app)

    app.run(host="127.0.0.1" if __LOCAL else "0.0.0.0", port=__PORT)
