
def __call__(app):

    @app.route("/")
    def root():

        return "Hello"
