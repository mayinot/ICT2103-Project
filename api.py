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


def init_connection_sql():
    '''
    Initialise connection for MySQL
    '''
    return mysql.connector.connect(host=constants.HOST,
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
        # print(f"{row}"
        payload.append(row)
    return payload


def dashboard_95percentile_POLY(connection_string) -> List:
    '''
    Query to get top 95 percentile grades of Polytechnic students applying for University courses

    Args:
        connection_string (object): The database location mysql connector
    Returns:
            list: a list of tuples representing the queried payload   
    '''

    payload = []
    query = '''
SELECT GP.Poly90thPerc, C.CourseName
FROM unify_db.GradeProfile GP, unify_db.Courses C
WHERE C.CourseID = GP.CourseID
ORDER BY GP.Poly90thPerc DESC
LIMIT 20;
    '''
    cur = connection_string.cursor()
    cur.execute(query)
    cursor = cur.fetchall()
    for row in cursor:
        # print(f"{row}")
        payload.append(row)

    return payload


def admin_viewAll(connection_string) -> List:
    '''
    Query to get all course details from all universities

    Args:
        connection_string (object): The database location mysql connector
    Returns:
            list: a list of tuples representing the queried payload   
    '''
    cur = connection_string.cursor()
    cur.execute('''
    SELECT C.CourseID,C.UniName,C.CourseName,
    G.Poly10thPerc,G.Poly90thPerc,G.Alevel10thPerc,G.Alevel90thPerc,
    intake,C.AvgGradPay 
    FROM unify_db.Courses C
    LEFT JOIN unify_db.GradeProfile G 
    ON C.CourseID = G.CourseID''')
    data = cur.fetchall()
    cur.close()
    connection_string.close()
    return data


if __name__ == "__main__":
    # API testing
    print(dashboard_salary(conn))
    print(dashboard_95percentile_POLY(conn))
    print(admin_viewAll(conn))
    pass
