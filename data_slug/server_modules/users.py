import mysql.connector as mariadb
import sql_commands

__USER_TABLE = "Users"


def has_any_users(project_connector):

    with project_connector as conn:

        cursor = conn.cursor

        if cursor:

            try:

                return cursor.select(
                    sql_commands.table_has_any,
                    project_connector.get_table(__USER_TABLE)) == "TRUE"

            except mariadb.Error:

                return False
    return False
