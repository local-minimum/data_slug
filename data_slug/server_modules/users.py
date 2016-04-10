import mysql.connector as mariadb
import sql_commands

__USER_TABLE = "Users"


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

            except mariadb.Error, e:
                print "No table"
                return False

            return cursor.fetchone() == "TRUE"
    return False
