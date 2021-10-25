from flask import Flask, render_template, url_for
from flask import Flask, render_template, request
from mysql import connector
import mysql.connector
from Credentials import constants

conn = mysql.connector.connect(host=constants.HOST,
        port=constants.PORT,
        database=constants.DATABASE,
        user=constants.USER,
        password=constants.PASSWORD
        )


app = Flask(__name__)
# index route 
@app.route('/')
def index():
    return render_template('index.html')

# dashboard routing 
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html') 

# courses route 
@app.route('/courses', methods=['GET','POST'])
def courses():
    conn = mysql.connector.connect(host=constants.HOST,
        port=constants.PORT,
        database=constants.DATABASE,
        user=constants.USER,
        password=constants.PASSWORD
        )
    cur = conn.cursor()
    # Select all courses for courses card
    result = cur.execute("""SELECT C.CourseName, C.CourseDesc, C.CourseURL, C.AvgGradPay, U.UniImage, F.FacultyName, C.UniName
                    FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F
                    WHERE C.UniName = U.UniName
                    AND C.FacultyID = F.FacultyID; """)
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
        salary = request.form.get('Salary')
        UNI_list = str(tuple([key for key in UniList])).replace(',)', ')')
        print(UNI_list)
        print(category)
        print(salary)
        query ="""SELECT C.CourseName, C.CourseDesc, C.CourseURL, C.AvgGradPay, U.UniImage, F.FacultyName, C.UniName 
        FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F,  unify_db.Category Ca, unify_db.FacultyCategory FC
        WHERE C.UniName = U.UniName
        AND C.FacultyID = F.FacultyID
        AND F.FacultyID = FC.FacultyID
        AND Ca.CategoryID = FC.CategoryID
        AND Ca.CategoryName = %s
        AND C.AvgGradPay > %s
        AND C.UniName IN {UNI_list};""".format(UNI_list=UNI_list)
        result= cur.execute(query, (category, salary))
        coursesinfo = cur.fetchall()


    cur.close()
    conn.close()
    return render_template('courses.html', coursesinfo=coursesinfo, categoryinfo=categoryinfo, uniinfo=uniinfo)

# admin route (create courses)
@app.route('/addcourses')
def addcourses():
    return render_template('addcourses.html')

# admin route (create courses)
@app.route('/editcourses')
def editcourses():
    return render_template('editcourses.html')
  
# admin route
@app.route('/adminLogin/')
def admin():
    return render_template('admin/adminLogin.html')

@app.route('/adminDash')
def adminDash():
    return render_template('admin/adminDashBoard.html')

@app.route('/adminViewData')
def adminViewData():
    return render_template('admin/adminViewData.html')

@app.route('/adminEditData')
def adminEditData():
    return render_template('admin/adminEditData.html')




if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)