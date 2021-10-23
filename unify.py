from flask import Flask, render_template, url_for
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 8809
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mayS9974536C'
app.config['MYSQL_DB'] = 'unify_db'
# init MYSQL
mysql = MySQL(app)










# index route 
@app.route('/')
def index():
    return render_template('index.html')

# dashboard routing 
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html') 

# courses route 
@app.route('/courses')
def courses():
    cur = mysql.connection.cursor()
    result = cur.execute("""SELECT C.CourseName, C.CourseDesc, C.CourseURL, C.AvgGradPay, U.UniImage, F.FacultyName 
                    FROM unify_db.Courses C, unify_db.University U, unify_db.Faculty F
                    WHERE C.UniName = U.UniName
                    AND C.FacultyID = F.FacultyID; """)
    if result > 0: 
        coursesinfo = cur.fetchall()
        return render_template('courses.html', coursesinfo=coursesinfo )
    mysql.connection.commit()
    cursor.close()
   

    


# admin route (create courses)
@app.route('/addcourses')
def addcourses():
    return render_template('addcourses.html')

# admin route (create courses)
@app.route('/editcourses')
def editcourses():
    return render_template('editcourses.html')
  
# admin route
@app.route('/admin-only/login/')
def admin():
    return render_template('admin/admin.html')

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