import pymysql
import os 
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
def execute_query(query, data=None, fetchone=False, is_insert=False):
    result = None

    try:
        with pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT')),
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
