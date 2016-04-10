#!/usr/bin/env python3

from flask import Flask, request


def get_app(local=False, port=80, debug=False):

    app = Flask("127.0.0.1" if local else "0.0.0.0", port=port)
    app.debug = debug
    return app

if __name__ == "__main__":

    app = get_app(local=True, debug=True)
    app.run()
