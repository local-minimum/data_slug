
def register_routes(app):

    @app.route("/")
    def root():

        return "Hello"

    @app.route("/logout", methods=("post", ))
    def logout():

        pass

    @app.route("/login", methods=("post",))
    def login():

        pass
