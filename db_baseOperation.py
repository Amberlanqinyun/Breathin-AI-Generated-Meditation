from db_credentials import db_config
import pymysql


def execute_query(query, data=None, fetchone=False, is_insert=False):
    # Establish a connection to the database using the db_config dictionary
    connection = None
    cursor = None
    result = None

    try:
        connection = pymysql.connect(
            host=db_config['db_host'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            db=db_config['db_name'],
            port=db_config['port']
        )
        # Create a cursor to interact with the database
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # If data is provided, execute the query with the data
        if data:
            cursor.execute(query, data)
        else:
            # If no data is provided, execute the query without data
            cursor.execute(query)
        
        # Commit/save changes to the database
        connection.commit()
        
        # Handle fetching result based on the provided parameters
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        # If it's an INSERT operation, get the last inserted row id
        if is_insert:
            result = cursor.lastrowid

    # If an error occurred, roll back the transaction
    except Exception as e:
        if connection:
            connection.rollback()
        print("Transaction did not complete. Please try again if the option is there for you to do so:", str(e))
    
    finally:
        # Close the cursor and the database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Return the fetched result if available
    return result
