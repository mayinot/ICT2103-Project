from typing import List
from mysql import connector
import mysql.connector
from Credentials import constants

# Connection String for Database
conn = mysql.connector.connect(host=constants.HOST,
                               database=constants.DATABASE,
                               user=constants.USER,
                               password=constants.PASSWORD
                               )


def dashboard_salary(connection_string) -> List:
    '''
    Query to get top 10 salary from the University courses

    Args:
        connection_string (object): The database location mysql connector
    Returns:
            list: a list of tuples representing the queried payload   
    '''

    payload = []
    query = '''
SELECT courseName, avgGradPay 
FROM unify_db.Courses
ORDER BY avgGradPay DESC
LIMIT 10;
    '''
    cur = connection_string.cursor()
    cur.execute(query)
    cursor = cur.fetchall()
    for row in cursor:
        # print(f"{row}")
        payload.append(row)
    return payload


def dashboard_95percentile(connection_string):
    '''hello'''


if __name__ == "__main__":
    print(dashboard_salary(conn))
