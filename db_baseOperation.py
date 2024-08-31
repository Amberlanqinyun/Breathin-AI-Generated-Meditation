from db_credentials import db_config
import pymysql

def execute_query(query, data=None, fetchone=False, is_insert=False):
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
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        
        connection.commit()
        
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        if is_insert:
            result = cursor.lastrowid

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error occurred during transaction: {str(e)}")
        print(f"Query: {query}")
        if data:
            print(f"Data: {data}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result
