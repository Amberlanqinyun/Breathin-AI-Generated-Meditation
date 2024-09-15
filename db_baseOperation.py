from db_credentials import db_config
import pymysql

def execute_query(query, data=None, fetchone=False, is_insert=False):
    result = None

    try:
        with pymysql.connect(
            host=db_config['db_host'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            db=db_config['db_name'],
            port=db_config['port'],
            cursorclass=pymysql.cursors.DictCursor
        ) as connection:
            with connection.cursor() as cursor:
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
        print(f"Error occurred during transaction: {str(e)}")
        print(f"Query: {query}")
        if data:
            print(f"Data: {data}")

    return result
