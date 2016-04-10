import mysql.connector as mariadb
import hashlib
import time
from enum import Enum  # enum34 module on python2.7
from flask import request, jsonify

import sql_commands

__USER_TABLE = "Users"


class UserTypes(Enum):

    owner = 0
    admin = 1
    user = 2
    guest = 3
    requested = 4


def has_any_users(project_connector):

    """

    :type project_connector: core.ProjectConnector
    """
    with project_connector as conn:

        cursor = conn.cursor
        if cursor is not None:
            try:

                cursor.execute(
                    sql_commands.table_has_any,
                    (project_connector.get_table_name(__USER_TABLE),))

            except mariadb.Error:
                print "No table"
                return False

            return cursor.fetchone() == "TRUE"
    return False


def sanity_check_password(user_name, user_password):

    # Stupidity check
    if user_name in user_password or user_password in user_name:
        return False

    # Complexity check
    if len(user_password) < 8 and set(c for c in user_password) < 5:
        return False

    # Wordlist check
    if user_password in ("1234567890", "123456789", "12345678", "password"):
        return False

    return True


def add_user(project_connector, user_name, user_type, user_password):
    """
    :type project_connector: core.ProjectConnector
    :type user_name: str
    :type user_type: Union[UserTypes, int]
    :type user_password: str
    """

    if not isinstance(user_type, UserTypes) or not sanity_check_password(user_name, user_password):

        return False

    with project_connector as conn:

        cursor = conn.cursor

        if cursor is None:

            return False

        else:

            try:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS %s
                        (user_id INT AUTO_INCREMENT PRIMARY_KEY,
                         user_type INT,
                         user_name VARCHAR UNIQUE,
                         user_password CHAR[64]
                         user_password_seed CHAR[64]);""")

            except mariadb.Error:
                print "Could not create user table"
                return False

            password_seed = hashlib.sha256(str(time.time())).hexdigest()
            password = hashlib.sha256(user_password + password_seed).hexdigest()
            cursor.execute(
                """INSERT INTO %s (user_type, user_name, user_password, user_password_seed)
                    VALUES (%i, %s, %s, %s);""", (user_type.value, user_name, password, password_seed))

            cursor.commit()
            return True


def register_routes(app):

    @app.route("/users/logout", methods=("POST", "GET"))
    def logout():

        return "Good-bye"

    @app.route("/users/login", methods=("POST", "GET"))
    def login():

        return "Hello"

    @app.route("/users/add", defaults={'project': ""}, methods=("POST",))
    @app.route("/users/add/", defaults={'project': ""}, methods=("POST",))
    @app.route("/<project>/users/add", methods=("POST",))
    @app.route("/<project>/users/add/", methods=("POST",))
    def add(project):

        global_connector = app.db[""]
        project_connector = app.db[project]

        lvl = UserTypes.owner if (not has_any_users(global_connector) and not has_any_users(project_connector)) else \
            UserTypes.requested

        success = add_user(
            project_connector,
            user_name=request.form['user_name'],
            user_password=request.form['user_password'],
            user_type=lvl)

        jsonify(success=success)

    print "Registered user actions"
