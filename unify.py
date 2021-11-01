from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from mysql import connector
import mysql.connector
from Credentials import constants

conn = mysql.connector.connect(host=constants.HOST,
                               database=constants.DATABASE,
                               user=constants.USER,
                               password=constants.PASSWORD
                               )


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# index route
@app.route('/', methods=['GET'])
def index():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    query = cur.execute("""SELECT U.UniName
                 FROM unify_db.University U
                 ORDER BY U.UniName; """)
    cur.execute(query)
    uniinfo = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", uniinfo=uniinfo)


@app.route('/', methods=['GET', 'POST'])
def home():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()

    if request.method == 'POST':
        UniInfo = request.form.get('uniinfo')
        CatInfo = request.form.get('category')

        Courses = cur.execute("""SELECT DISTINCT C.CourseName
                 FROM unify_db.Category Ca, unify_db.FacultyCategory FC, unify_db.Faculty F, unify_db.Courses C
                 WHERE C.UniName =  %s
                 AND C.FacultyID = F.FacultyID
                 AND FC.FacultyID = F.FacultyID
                 AND FC.CategoryID = %s
                 ORDER BY C.CourseName;""", (UniInfo, CatInfo, ))
        coursesinfo = cur.fetchall()
        cur.close()
        conn.close()
        return redirect(url_for("courses", Courses=coursesinfo))
        # return render_template("courses.html", uni=UniInfo, cat=CatInfo)
        # return render_template("courses.html", courses=Courses)
    else:
        cur.close()
        conn.close()
        return render_template("index.html")
    
# Get the category according to the university
@app.route('/<getCat>')
def categoryByUniversity(getCat):
    conn = mysql.connector.connect(host=constants.HOST,
                                port=constants.PORT,
                                database=constants.DATABASE,
                                user=constants.USER,
                                password=constants.PASSWORD
                                )
    cur = conn.cursor()
    # The database will use the specified type and value of getCat when executing the query, 
    # offering protection from Python SQL injection.
    result = cur.execute("""SELECT DISTINCT Ca.CategoryName
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
    return jsonify({'categoryList' : categoryArray})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# get courses from index route 
@app.route('/<Courses>', methods=['GET', 'POST'])
def getIndexCourses(Courses):
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()


    # Select the category for dropdown
    result = cur.execute("""SELECT CategoryName
                    FROM unify_db.Category; """)
    categoryinfo = cur.fetchall()
    # Select the uniname for check box
    result = cur.execute("""SELECT UniName
                    FROM unify_db.University; """)
    uniinfo = cur.fetchall()

    # query = """SELECT C.CourseName, C.CourseDesc, C.CourseURL, IFNULL(NULLIF(CAST(C.AvgGradPay AS char), "0"), "N/A") as AvgGradPay, U.UniImage, F.FacultyName, C.UniName 
    #     FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F,  unify_db.Category Ca, unify_db.FacultyCategory FC
    #     WHERE C.UniName = %s
    #     AND C.FacultyID = F.FacultyID
    #     AND F.FacultyID = FC.FacultyID
    #     AND Ca.CategoryID = FC.CategoryID
    #     AND Ca.CategoryName = %s
    #     ;"""
    # result = cur.execute(query, (uni, cat, ))
    # coursesinfo = cur.fetchall()

    result = cur.execute(Courses)
    coursesinfo = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('courses.html', coursesinfo=coursesinfo, categoryinfo=categoryinfo, uniinfo=uniinfo)



# courses route
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    # Select all courses for courses card
    result = cur.execute("""SELECT C.CourseName, C.CourseDesc, C.CourseURL, IFNULL(NULLIF(CAST(C.AvgGradPay AS char), "0"), "N/A") as AvgGradPay, U.UniImage, F.FacultyName, C.UniName
                    FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F
                    WHERE C.UniName = U.UniName
                    AND C.FacultyID = F.FacultyID;""")
    coursesinfo = cur.fetchall()
    # Select the category for dropdown
    result = cur.execute("""SELECT CategoryName
                    FROM unify_db.Category; """)
    categoryinfo = cur.fetchall()
    # Select the uniname for check box
    result = cur.execute("""SELECT UniName
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
        query = """SELECT C.CourseName, C.CourseDesc, C.CourseURL, IFNULL(NULLIF(CAST(C.AvgGradPay AS char), "0"), "N/A") as AvgGradPay, U.UniImage, F.FacultyName, C.UniName 
        FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F,  unify_db.Category Ca, unify_db.FacultyCategory FC
        WHERE C.UniName = U.UniName
        AND C.FacultyID = F.FacultyID
        AND F.FacultyID = FC.FacultyID
        AND Ca.CategoryID = FC.CategoryID
        AND Ca.CategoryName = %s
        AND C.AvgGradPay >= %s
        AND C.AvgGradPay <= %s
        AND C.UniName IN {UNI_list};""".format(UNI_list=UNI_list)
        result = cur.execute(query, (category, FROMsalary, TOsalary))
        coursesinfo = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('courses.html', coursesinfo=coursesinfo, categoryinfo=categoryinfo, uniinfo=uniinfo)

# admin route (create courses)


@app.route('/addcourses')
def addcourses():
    return render_template('addcourses.html')

# admin route (create courses)


@app.route('/editcourses', methods=['GET', 'POST'])
def editcourses():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        print(CourseID)
        query = """SELECT  C.CourseName, C.CourseDesc, C.CourseURL, C.AvgGradPay, C.CourseID
        FROM unify_db.Courses C
        WHERE C.CourseID = %s """
        result = cur.execute(query, (CourseID,))
        Editcoursesinfo = cur.fetchone()
        print(Editcoursesinfo)
    cur.close()
    conn.close()
    return render_template('editcourses.html', Editcoursesinfo=Editcoursesinfo)

# admin route
@app.route('/adminLogin/')
def admin():
    return render_template('admin/adminLogin.html')


@app.route('/adminDash')
def adminDash():
    return render_template('admin/adminDashBoard.html')


@app.route('/adminViewData')
def adminViewData():
    conn = mysql.connector.connect(host=constants.HOST,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    cur.execute("""SELECT C.CourseID,C.UniName,C.CourseName,
    G.Poly10thPerc,G.Poly90thPerc,G.Alevel10thPerc,G.Alevel90thPerc,
    intake,C.AvgGradPay 
    FROM unify_db.Courses C
    LEFT JOIN unify_db.GradeProfile G 
    ON C.CourseID = G.CourseID""")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin/adminViewData.html', data=data)


@app.route('/adminEditData/<Course_ID>', methods=['GET', 'POST'])
def adminEditData(Course_ID):
    if(request.method == 'GET'):
        print(Course_ID)
        conn = mysql.connector.connect(host=constants.HOST,
                                       database=constants.DATABASE,
                                       user=constants.USER,
                                       password=constants.PASSWORD
                                       )
        cur = conn.cursor()
        cur.execute("""SELECT C.CourseName,G.Poly10thPerc,G.Poly90thPerc,G.Alevel10thPerc,G.Alevel90thPerc,intake,C.AvgGradPay 
        FROM unify_db.Courses C, unify_db.GradeProfile G 
        WHERE C.CourseID = %s """, (Course_ID))
        # query = """SELECT C.CourseName,G.Poly10thPerc,G.Poly90thPerc,G.Alevel10thPerc,G.Alevel90thPerc,intake,C.AvgGradPay FROM unify_db.Courses C, unify_db.GradeProfile G
        # # WHERE C.CourseID = %s """.format(Course_ID)
        # cur.execute(query)
        dataToEdit = cur.fetchall()
        print(dataToEdit)
        cur.close()
        conn.close()
        return render_template('admin/adminEditData.html', dataToEdit=dataToEdit)
    # else:

# admin route


@app.route('/SuccessfulEdit', methods=['GET', 'POST'])
def SuccessfulEdit():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        CourseName = request.form.get('CourseName')
        CourseURL = request.form.get('CourseURL')
        CourseSalary = request.form.get('AvgGradPay')
        CourseDesc = request.form.get('CourseDesc')
        cur.execute("""  UPDATE unify_db.Courses C
                    SET C.CourseName = %s, C.CourseDesc = %s, C.CourseURL = %s, C.AvgGradPay = %s
                    WHERE C.CourseID = %s""",
                    (CourseName, CourseDesc, CourseURL, CourseSalary, CourseID,))
        conn.commit()
    cur.close()
    conn.close()

    return render_template('admin/SuccessfulEdit.html')


# admin route
@app.route('/deletecourses', methods=['GET', 'POST'])
def deletecourses():
    conn = mysql.connector.connect(host=constants.HOST,
                                   port=constants.PORT,
                                   database=constants.DATABASE,
                                   user=constants.USER,
                                   password=constants.PASSWORD
                                   )
    cur = conn.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        print(CourseID)
        cur.execute("""DELETE FROM unify_db.Courses C 
                        WHERE C.CourseID =%s """,
                    (CourseID,))
        conn.commit()
    cur.close()
    conn.close()
    return render_template('deletecourses.html')


if __name__ == "__main__":
    # Error will be displayed on web page
    app.run(debug=True)
