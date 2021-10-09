import sqlite3 
from sqlite3 import Error
import os 

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

out = os.path.join(os.getcwd(), 'static', 'database', 'test.db')

if __name__ == '__main__':
    create_connection(r"static\database\test.db")
    conn = sqlite3.connect(out)
    stmt = '''SELECT * FROM myTable'''
    cursor = conn.execute(stmt)
    for row in cursor:
      print(f"{row}")
    print("Operation done successfully")
 


