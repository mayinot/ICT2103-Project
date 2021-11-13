from typing import List
from mysql import connector
import mysql.connector
from Credentials import constants
from flask import request, flash, redirect, url_for, jsonify


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
    Query to get all course details from all universities for admins

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


def course_query(connection_string) -> List:
    '''
    Query to get all course details from all universities for users

    Args:
        connection_string (object): The database location mysql connector
    Returns:
            list: a list of tuples representing the queried payload   
    '''
    cur = connection_string.cursor()
    # Select all courses for courses card
    cur.execute("""
                    SELECT C.CourseName, C.CourseDesc, C.CourseURL, IFNULL(NULLIF(CAST(C.AvgGradPay AS char), "0"), "N/A") as AvgGradPay, U.UniImage, F.FacultyName, C.UniName
                    FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F
                    WHERE C.UniName = U.UniName
                    AND C.FacultyID = F.FacultyID;""")
    coursesinfo = cur.fetchall()
    # Select the category for dropdown
    cur.execute("""SELECT CategoryName
                    FROM unify_db.Category;""")
    categoryinfo = cur.fetchall()
    # Select the uniname for check box
    cur.execute("""SELECT UniName
                    FROM unify_db.University; """)
    uniinfo = cur.fetchall()

    if request.method == 'POST':
        UniList = request.form.getlist('UniFilter')
        category = request.form.get('category')
        FROMsalary = request.form.get('fromSalary')
        TOsalary = request.form.get('toSalary')
        if TOsalary < FROMsalary:
            flash('To Salary cannot be more than From Salary!')
            redirect(url_for('courses'))
        UNI_list = str(tuple([key for key in UniList])).replace(',)', ')')
        print(UNI_list)
        print(category)
        query = """
        SELECT C.CourseName, C.CourseDesc, C.CourseURL, IFNULL(NULLIF(CAST(C.AvgGradPay AS char), "0"), "N/A") as AvgGradPay, U.UniImage, F.FacultyName, C.UniName 
        FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F,  unify_db.Category Ca, unify_db.FacultyCategory FC
        WHERE C.UniName = U.UniName
        AND C.FacultyID = F.FacultyID
        AND F.FacultyID = FC.FacultyID
        AND Ca.CategoryID = FC.CategoryID
        AND Ca.CategoryName = %s
        AND C.AvgGradPay >= %s
        AND C.AvgGradPay <= %s
        AND C.UniName IN {UNI_list};""".format(UNI_list=UNI_list)
        cur.execute(query, (category, FROMsalary, TOsalary))
        coursesinfo = cur.fetchall()
    cur.close()
    connection_string.close()
    return coursesinfo, categoryinfo, uniinfo


def editcourse_query(connection_string) -> List:
    '''
    Query to editing course

    Args:
        connection_string (object): The database location mysql connector
    Returns:
            list: a list of tuples representing the queried payload   
    '''
    cur = connection_string.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        print(CourseID)
        query = """SELECT  C.CourseName, C.CourseDesc, C.CourseURL, C.AvgGradPay, C.CourseID
        FROM unify_db.Courses C
        WHERE C.CourseID = %s """
        cur.execute(query, (CourseID,))
        Editcoursesinfo = cur.fetchone()
        print(Editcoursesinfo)
    cur.close()
    connection_string.close()
    return Editcoursesinfo


def categorise_uni(connection_string, getCat):
    cur = connection_string.cursor()
    # The database will use the specified type and value of getCat when executing the query,
    # offering protection from Python SQL injection.
    cur.execute("""
                    SELECT DISTINCT Ca.CategoryName
                    FROM unify_db.Category Ca, unify_db.FacultyCategory FC, unify_db.Faculty F, unify_db.Courses C
                    WHERE Ca.CategoryID = FC.CategoryID
                    AND FC.FacultyID = F.FacultyID
                    AND C.FacultyID = F.FacultyID
                    AND C.UniName = %s
                    ORDER BY Ca.CategoryName
                    ;""", (getCat, ))
    category = cur.fetchall()
    categoryArray = []
    for row in category:
        categoryObj = {
            'id': row[0],
            'name': row[0]
        }
        categoryArray.append(categoryObj)
    return jsonify({'categoryList': categoryArray})


if __name__ == "__main__":
    # API testing
    print(dashboard_salary(conn))
    print(dashboard_95percentile_POLY(conn))
    print(admin_viewAll(conn))
    print(course_query(conn))
    print(editcourse_query(conn))
    print(categorise_uni(conn))
    pass
