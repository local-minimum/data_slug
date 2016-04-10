import mysql.connector as mariadb

__USER_TABLE = "Users"


def has_any_users(app):

    cursor = app.db.cursor
    if cursor:

        try:
            cursor.select()
        except mariadb.Error:
            return False
        else:
            return True
    return False
