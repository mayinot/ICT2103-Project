from flask import Flask, render_template, request, redirect, url_for
from mysql import connector
import mysql.connector
from Credentials import constants
import api
import api_mongo
import pymongo

app = Flask(__name__)
# For pop up
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# index route


#----------------------------------------------------------------SQL Pages Routes------------------------------------------------------------------------------------------------------------#
@app.route('/', methods=['GET'])
def index():
    conn = api.init_connection_sql()
    uniFilter = api.univeristy_query(conn)
    conn.close()
    return render_template("/Sql/index.html", uniFilter=uniFilter)


@app.route('/<getUniCat>')
def categoryByUniversity(getUniCat):
    conn = api.init_connection_sql()
    cat_list = api.categorise_uni(conn, getUniCat)
    conn.close()
    return (cat_list)

# dashboard routing


@app.route('/dashboard')
def dashboard():
    conn = api.init_connection_sql()
    # data parsing for top 10 salary in dashboard
    payload_salary = api.dashboard_salary(conn)
    salary_labels = [row[0] for row in payload_salary]
    salary_values = [row[1] for row in payload_salary]

    # data parsing for top 95 percentile for polytechnic applicants into university
    payload_polypercentile = api.dashboard_95percentile_POLY(conn)
    ppercentile_labels = [row[1] for row in payload_polypercentile]
    ppercentile_values = [row[0] for row in payload_polypercentile]

    # data parsing for intake data
    intake_data = api.query_intake(conn)
    total_intake = api.sum_intake(conn)

    # data parsing for total records
    records = api.all_data_count(conn)
    records = sum([row[0] for row in records])

    # data parsing for total number of courses
    total_courses = api.total_course(conn)
    total_courses = sum([row[0] for row in total_courses])

    # data parsing for total number of universities
    total_uni = api.total_uni(conn)
    total_uni = sum([row[0] for row in total_uni])

    return render_template('/Sql/dashboard.html', labels=salary_labels, values=salary_values,
                           ppercentile_labels=ppercentile_labels, ppercentile_values=ppercentile_values,
                           intake_data=intake_data, records=records, total_intake=total_intake,
                           total_courses=total_courses, total_uni=total_uni)

# courses route


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    conn = api.init_connection_sql()
    coursesinfo, categoryinfo, uniinfo = api.course_query(conn)
    return render_template('/Sql/courses.html', coursesinfo=coursesinfo, categoryinfo=categoryinfo, uniinfo=uniinfo)

# admin route (create courses)
@app.route('/addcourses')
def addcourses():
    return render_template('/Sql/admin/addcourses.html')

# admin route (edit courses)
@app.route('/editcourses', methods=['GET', 'POST'])
def editcourses():
    conn = api.init_connection_sql()
    edit_query = api.editcourse_query(conn)
    return render_template('/Sql/admin/editcourses.html', Editcoursesinfo=edit_query)

#admin route (dashboard)
@app.route('/adminDash')
def adminDash():
    return render_template('/Sql/admin/adminDashBoard.html')

#admin route (view detail of the courses)
@app.route('/adminViewData')
def adminViewData():
    conn = api.init_connection_sql()
    data = api.admin_viewAll(conn)
    return render_template('/Sql/admin/adminViewData.html', data=data)


@app.route('/adminEditData/<Course_ID>', methods=['GET', 'POST'])
def adminEditData(Course_ID):
    if(request.method == 'GET'):
        print(Course_ID)
        conn = api.init_connection_sql()
        cur = conn.cursor()
        cur.execute("""
        SELECT C.CourseName,G.Poly10thPerc,G.Poly90thPerc,G.Alevel10thPerc,G.Alevel90thPerc,intake,C.AvgGradPay 
        FROM unify_db.Courses C, unify_db.GradeProfile G 
        WHERE C.CourseID = %s """, (Course_ID))
        dataToEdit = cur.fetchall()
        print(dataToEdit)
        cur.close()
        conn.close()
        return render_template('/Sql/admin/adminEditData.html', dataToEdit=dataToEdit)
    # else:

# admin route


@app.route('/adminAddCourse', methods=['GET', 'POST'])
def adminAddCourse():
    conn = api.init_connection_sql()
    cur = conn.cursor()
    cur.execute("SELECT UniName FROM unify_db.University;")
    universities = cur.fetchall()
    cur.execute("SELECT FacultyID, FacultyName FROM unify_db.Faculty;")
    Faculties = cur.fetchall()
    if request.method == 'POST':
        university = request.form.get('university')
        facultyID = request.form.get('Faculty')
        courseName = request.form.get('course')
        CourseURL = request.form.get('course_url')
        CourseDesc = request.form.get('description')
        CourseID = request.form.get('courseID')
        poly10 = request.form.get('poly10')
        poly90 = request.form.get('poly90')
        Alevel10 = request.form.get('Alevel10')
        Alevel90 = request.form.get('Alevel90')
        intake = request.form.get('intake')
        avgpay = request.form.get('avgpay')
        FacultyID = request.form.get('FacultyID')
        print(courseName, CourseDesc, CourseID,
              CourseURL, avgpay, intake, university,facultyID)
        cur.execute("""INSERT INTO unify_db.Courses(CourseName,CourseDesc,CourseID,CourseURL,AvgGradPay,Intake,UniName,FacultyID ) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",(courseName,CourseDesc,CourseID,CourseURL,avgpay,intake,university,facultyID))
        conn.commit()
        cur.execute("""INSERT INTO unify_db.GradeProfile(poly10thPerc,poly90thPerc,Alevel90thPerc,Alevel10thPerc,CourseID)
             VALUES(%s,%s,%s,%s,%s)""",(poly10,poly90,Alevel10,Alevel90,CourseID,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('adminViewData'))
    return render_template('/Sql/admin/adminAddCourse.html', universities=universities, Faculties=Faculties)



@app.route('/SuccessfulEdit', methods=['GET', 'POST'])
def SuccessfulEdit():
    conn = api.init_connection_sql()
    cur = conn.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        CourseName = request.form.get('CourseName')
        CourseURL = request.form.get('CourseURL')
        CourseSalary = request.form.get('AvgGradPay')
        CourseDesc = request.form.get('CourseDesc')
        cur.execute(""" 
                    UPDATE unify_db.Courses C
                    SET C.CourseName = %s, C.CourseDesc = %s, C.CourseURL = %s, C.AvgGradPay = %s
                    WHERE C.CourseID = %s""",
                    (CourseName, CourseDesc, CourseURL, CourseSalary, CourseID,))
        conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('adminViewData'))
    #return render_template('/Sql/admin/SuccessfulEdit.html')


# admin route
@app.route('/deletecourses', methods=['GET', 'POST'])
def deletecourses():
    conn = api.init_connection_sql()
    cur = conn.cursor()
    if request.method == 'POST':
        CourseID = request.form.get('CourseId')
        print(CourseID)
        cur.execute("""
                        DELETE FROM unify_db.Courses C 
                        WHERE C.CourseID = %s """,
                    (CourseID,))
        conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('adminViewData'))
    #return render_template('/Sql/admin/deletecourses.html')


#--------------------------------------------------------------NoSQL Pages Routes------------------------------------------------------------------------------------------------------------#
@app.route('/index_NoSql', methods=['GET'])
def index_NoSql():
    uniFilter = api_mongo.fetch_Uninames()
    return render_template("/NoSql/index-NoSql.html",  uniFilter=uniFilter)


@app.route('/index_NoSql/<getUniCat>')
def categoryByUniversity_NoSql(getUniCat):
    categoryinfo = api_mongo.fetch_CategoryNames(getUniCat)
    return (categoryinfo)


@app.route('/courses_NoSql', methods=['GET', 'POST'])
def courses_NoSql():
    coursesinfo = api_mongo.fetch_Courses()
    uniinfo = api_mongo.fetch_Uninames()
    categoryinfo = api_mongo.fetch_CategoryNames_Raw()
    # Get Form data
    if request.method == 'POST':
        UniList = request.form.getlist('uniFilter')
        category = request.form.get('category')
        FROMsalary = request.form.get('fromSalary')
        TOsalary = request.form.get('toSalary')
        coursesinfo = api_mongo.filter_Course(
            UniList, category, FROMsalary, TOsalary)
        print(coursesinfo)
        return render_template('/NoSql/courses-NoSql.html', coursesinfo=coursesinfo, uniinfo=uniinfo, categoryinfo=categoryinfo)
    return render_template('/NoSql/courses-NoSql.html', coursesinfo=coursesinfo, uniinfo=uniinfo, categoryinfo=categoryinfo)


@app.route('/dashboard_NoSql')
def dashboard_NoSql():
    # data parsing for top 10 salary
    dataset = api_mongo.top_salary()
    course_name = []
    salary = []
    for i in range(len(dataset)):
        course_name.append(dataset[i]['CourseName'])
        salary.append(dataset[i]['AvgGradPay'])

    # data parsing for top 95 % grades in poly
    grades = api_mongo.top_grade()
    course_name_poly = []
    poly_grade = []
    for i in range(len(grades)):
        course_name_poly.append(grades[i]['CourseName'])
        poly_grade.append(grades[i]['GradeProfile']['Poly90thPerc'])

    # data parsing for stats card
    documents = api_mongo.count_docs()
    total_courses = api_mongo.total_courses()
    total_intake = api_mongo.total_intake()
    total_uni = api_mongo.uni_total()

    # Table data
    intake_data = api_mongo.dashboard_table()

    return render_template('/NoSql/dashboard-NoSql.html', labels=course_name, values=salary,
                           course_name_poly=course_name_poly, poly_grade=poly_grade,
                           documents=documents, total_courses=total_courses,
                           total_intake=total_intake, total_uni=total_uni,
                           intake_data=intake_data)


@app.route('/adminDash_NoSql')
def adminDash_NoSql():
    return render_template('/NoSql/admin/adminDashBoard-NoSql.html')


@app.route('/adminViewData_NoSql', methods=['GET', 'POST'])
def adminView_NoSql():
    coursesinfo = api_mongo.fetch_Courses()
    return render_template('/NoSql/admin/adminViewData-NoSql.html', coursesinfo=coursesinfo)


@app.route('/adminAddCourse_NoSql', methods=['GET', 'POST'])
def adminAdd_NoSql():
    uniInfo = api_mongo.fetch_Uninames()
    if request.method == 'POST':
        api_mongo.insert_Course()
        return redirect(url_for('adminView_NoSql'))
    return render_template('/NoSql/admin/adminAddCourse-NoSql.html', uniInfo=uniInfo)


@app.route('/adminEditData_NoSql', methods=['GET', 'POST'])
def adminEdit_NoSql():
    CourseID = request.form.get('CourseId')
    courseInfo = api_mongo.fetchById(CourseID)
    return render_template('/NoSql/admin/adminEditCourse-NoSql.html', courseInfo=courseInfo, CourseID=CourseID)


@app.route('/adminDeleteCourse_NoSql', methods=['GET', 'POST'])
def adminDelete_NoSql():
    CourseID = request.form.get('CourseId')
    api_mongo.delete_Course(CourseID)
    return redirect(url_for('adminView_NoSql'))


@app.route('/successfulEdit_NoSql', methods=['GET', 'POST'])
def successfulEdit_NoSql():
    if request.method == 'POST':
        CourseID = request.form.get('CourseID')
        CourseName = request.form.get('CourseName')
        CourseURL = request.form.get('CourseURL')
        AvgGradPay = request.form.get('AvgGradPay')
        CourseDesc = request.form.get('CourseDesc')
        api_mongo.edit_Course(CourseID, CourseName,
                              CourseURL, AvgGradPay, CourseDesc)
        return redirect(url_for('adminView_NoSql'))


if __name__ == "__main__":
    # Error will be displayed on web page
    app.run(debug=True)
