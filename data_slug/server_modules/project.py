import sql_commands
import mysql.connector as mariadb
from warnings import warn
from users import UserTypes
from string import digits, letters

__DEFAULT_USER_JOIN_LEVEL = UserTypes.requested
__DEFAULT_LISTING_PROJECT = True

__PROJECTS_TABLE = "Projects"
__INVALID_NAMES = ("api", "static")
__ACCEPTABLE_CHARACTERS = digits + letters + "-_"


def _valid_project_name(project):
    """

    :param project: name of project
    :type project : str
    :return: If acceptable
    """
    if project.lower() in __INVALID_NAMES:
        warn("Word is reserved")
        return False

    return all(c in __ACCEPTABLE_CHARACTERS for c in project)


def has_any_project():

    return False


def is_setup():

    return False


def has_project(app, project):

    project_connector = app.db[""]
    with project_connector as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT project_name
            FROM %s WHERE project_name = %s LIMIT 1;
            """, tuple(__PROJECTS_TABLE, project))

        except mariadb.Error:
            return False

        return cursor.fetchone() == project

    return True


def create_project(app, project):

    if not _valid_project_name(project):
        warn("Name not valid")
        return False

    if has_project(project):
        warn("Attempt at creating existing project")
        return False

    return register_project(app, project)


def register_project(app, project):

    global_connector = app.db[""]
    with global_connector as connection:
        cursor = connection.cursor()
        if cursor is None:
            warn("No SQL privileges")
            return False

        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s
                    (project_id INT AUTO_INCREMENT PRIMARY_KEY,
                     project_name VARCHAR[16] UNIQUE NOT NULL,
                     project_full_name VARCHAR,
                     project_description TEXT,
                     creation_date DATETIME,
                     listing BOOL,
                     new_user_level INT[8]);""", tuple(__PROJECTS_TABLE))
        except mariadb.Error, e:
            warn("Failed to create table")
            return False

        cursor.execute(
            """INSERT INTO %s (project_name, creation_date, listing, new_user_level)
                VALUES (%s, CURRENT_DATE(), %b, %i);""",
            tuple(__PROJECTS_TABLE, project, __DEFAULT_LISTING_PROJECT, __DEFAULT_USER_JOIN_LEVEL.value))

        cursor.commit()

    return True


def get_all_public_projects():

    return []
