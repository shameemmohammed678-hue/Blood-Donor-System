import os
import pymysql
from config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_connection():
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=4000,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            ssl={
                "ca": os.path.join(BASE_DIR, "certs", "isrgrootx1.pem")
            },
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print("Database Connection Failed:", e)
        return None
           
if __name__ == "__main__":
    con = get_connection()
    if con:
        print("Database connected successfullly")
    else:
        print("Failed to connnect with database")
        