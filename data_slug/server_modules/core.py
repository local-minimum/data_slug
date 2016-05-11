import mysql.connector as mariadb
import warnings
from flask import send_from_directory, redirect
import os
import project

__STATIC_DIRECTORY = "static"
__JS_DIRECTORY = os.path.join(__STATIC_DIRECTORY, "js")
__IMAGE_DIRECTORY = os.path.join(__STATIC_DIRECTORY, "image")
__CSS_DIRECTORY = os.path.join(__STATIC_DIRECTORY, "css")
__HTML_DIRECTORY = os.path.join(__STATIC_DIRECTORY, "html")
__TEMPLATE_DIRECTORY = "templates"

__DB_USER = "data_slugger"
__DB_PWD = "ataminimumyouneedtochangethis"
__DB = "data_slug"

"""SQL commands that go with above settings (but change password!)

CREATE DATABASE IF NOT EXISTS data_slug;
CREATE USER 'data_slugger'@'localhost' IDENTIFIED WITH 'ataminimumyouneedtochangethis';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP ON data_slug.* TO 'data_slugger'@'localhost';
"""


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

        return self.__connection

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            if self.__connection:
                self.__connection.close()
                self.__connection = None
        else:
            self.__connection = None
            warnings.warn("Connection Error {0}: ({1})".format(exc_val, exc_tb))

    def get_table_name(self, table):

        if self.__project:
            table = "_".join((self.__project, table))
        if self.__connection_data.table_prefix:
            table = "_".join((self.__connection_data.table_prefix, table))
        return table

    @property
    def connected(self):

        return self.__connection is not None


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


def set_database_connector(app):

    app.db = ConnectionData(__DB_USER, __DB_PWD, __DB)


def register_routes(app):

    @app.route("/")
    def root():

        # Project with not name is the super-project

        if not project.is_setup():
            return redirect("/static/html/register_owner.html")

        elif not project.has_any_project():
            return redirect("/static/html/create_project.html")

        elif not "logged in":
            # TODO: Implement this
            public_projects = project.get_all_public_projects()
            return public_projects

        else:
            # TODO: Stitch dashboard, and projects something
            return None

    @app.route("/static/js/<js_file>")
    def get_js_file(js_file):

        return send_from_directory(__JS_DIRECTORY, js_file)

    @app.route("/static/image/<image_file>")
    def get_image_file(image_file):

        return send_from_directory(__IMAGE_DIRECTORY, image_file)

    @app.route("/static/css/<css_file>")
    def get_css_file(css_file):

        return send_from_directory(__CSS_DIRECTORY, css_file)

    @app.route("/static/html/<html_file>")
    def get_html_file(html_file):

        return send_from_directory(__HTML_DIRECTORY, html_file)
