import sqlite3 
from sqlite3 import Error
import os 
import mysql.connector
from Credentials import constants

def create_connection():
    """ create a database connection to a 
    SQLite database """
    conn = None
    try:
        # conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
        # Connecting to mysql database
        conn = mysql.connector.connect(host=constants.HOST, 
        database=constants.DATABASE,
        user=constants.USER,
        password=constants.PASSWORD
        )
        if conn.is_connected():
            db_Info = conn.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        # print(e)
        print("Error while connecting to MySQL", e)
    finally:
        if conn:
            conn.close()

out = os.path.join(os.getcwd(), 'static', 'database', 'test.db')

if __name__ == '__main__':
    # create_connection(r"static\database\test.db")
    create_connection()
    # conn = sqlite3.connect(out)
    conn = mysql.connector.connect(host=constants.HOST,
        database=constants.DATABASE,
        user=constants.USER,
        password=constants.PASSWORD
        )

    stmt = '''SELECT * FROM testdb'''
    cur = conn.cursor()
    cur.execute(stmt)
    cursor = cur.fetchall()
    for row in cursor:
      print(f"{row}")
    print("Operation done successfully")
 


 