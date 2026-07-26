import pymysql
from config import Config

def get_connection():
    try:
        connection = pymysql.connect(
            host = Config.MYSQL_HOST,
            user= Config.MYSQL_USER,
            password = Config.MYSQL_PASSWORD,
            database= Config.MYSQL_DB,
            cursorclass = pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print("Database Connection Failed",e)
        return None
           
if __name__ == "__main__":
    con = get_connection()
    if con:
        print("Database connected successfullly")
    else:
        print("Failed to connnect with database")