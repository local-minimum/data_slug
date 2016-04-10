import mysql.connector as mariadb
import sql_commands

__USER_TABLE = "Users"


def has_any_users(app, project=""):

    cursor = app.db.cursor
    if cursor:

        try:
            return cursor.select(
                sql_commands.table_has_any,
                app.db.get_table(__USER_TABLE, project)) == "TRUE"
        except mariadb.Error:
            return False
    return False
