import pymysql
from db_credentials import db_config

def execute_query(query, data=None, fetchone=False, is_insert=False):
    """
    Execute a SQL query with optional data for parameterized queries.

    Args:
        query (str): The SQL query to execute.
        data (tuple): The data to use in the query, if any.
        fetchone (bool): Whether to fetch a single result.
        is_insert (bool): Whether the query is an insert operation.

    Returns:
        result: The result of the query, if applicable.
    """
    connection = None
    cursor = None
    result = None

    try:
        # Establish a database connection
        connection = pymysql.connect(
            host=db_config['db_host'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            db=db_config['db_name'],
            port=db_config['port'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()

        # Execute the query with data, if provided
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        # Commit changes if it's an insert operation
        if is_insert:
            connection.commit()
            result = cursor.lastrowid
        else:
            result = cursor.fetchone() if fetchone else cursor.fetchall()

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error executing query: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result
