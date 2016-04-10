import mysql.connector as mariadb
import warnings

import users

__DB_USER = "data_slugger"
__DB_PWD = "hellokitty"
__DB = "data_slug"


class ProjectConnector(object):

    def __init__(self, connection_data, project):

        """

        :type project: str
        :type connection_data: ConnectionData
        """
        self.__connection_data = connection_data
        self.__project = project
        self.__connection = None

    def __enter__(self):

        if self.__connection is None:
            self.__connection = mariadb.connect(
                user=self.__connection_data.user,
                password=self.__connection_data.password,
                database=self.__connection_data.db)
        else:
            warnings.warn("Connection is already active, can't have two at a the same time")
            raise mariadb.Error(msg="Previous connection not closed")

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            if self.__connection:
                self.__connection.close()
                self.__connection = None
        else:
            self.__connection = None
            warnings.warn("Connection Error {0}: ({1})".format(exc_val, exc_tb))

    def get_table_name(self, table, project_name=""):

        if project_name:
            table = "_".join((project_name, table))
        if self.__connection_data.table_prefix:
            table = "_".join((self.__connection_data.table_prefix, table))
        return table

    @property
    def connected(self):

        return self.__connection is not None

    @property
    def cursor(self):

        if self.__connection:
            return self.__connection.cursor()
        return None


class ConnectionData(object):

    def __init__(self, user, password, db):

        self.user = user
        self.password = password
        self.db = db
        self.table_prefix = ""

    def __getitem__(self, project):

        """

        :param project: Name of the project to work with
         :type project : str
        :return: Project Connector
         :rtype : ProjectConnector
        """
        return ProjectConnector(self, project)


def monkey_patch_app(app):

    app.db = ConnectionData(__DB_USER, __DB_PWD, __DB)


def register_routes(app):

    @app.route("/")
    def root():

        project_connector = app.db["dev"]

        if users.has_any_users(project_connector):
            pass

        return "Hello"

    @app.route("/logout", methods=("post", ))
    def logout():

        pass

    @app.route("/login", methods=("post",))
    def login():

        pass
