import users
import mysql.connector as mariadb

__DB_USER = "data_slugger"
__DB_PWD = "hellokitty"
__DB = "data_slug"


class DBConnection(object):

    def __init(self, user, password, db):

        self.__user = user
        self.__password = password
        self.table_prefix = ""
        self.__connection = mariadb.connect(user=user, password=password,
                                            database=db)

    @property
    def cursor(self):

        if self.__connection:
            return self.__connection.cursor()
        return None

    def get_table_name(self, table, project_name=""):

        if project_name:
            table = "_".join(project_name, table)
        if self.table_prefix:
            table = "_".join(self.table_prefix, table)
        return table


def monkey_patch_app(app):

    app.db = DBConnection(__DB_USER, __DB_PWD, __DB)


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
