from flask import Flask, render_template, url_for
from mysql import connector
import mysql.connector
from Credentials import constants

conn = mysql.connector.connect(host=constants.HOST,
        database=constants.DATABASE,
        user=constants.USER,
        password=constants.PASSWORD
        )
# Set up our application (ref this file)
app = Flask(__name__)

# index route 
@app.route('/')
def adminDashboard():
    return render_template('adminDashBoard.html')

# index route 
@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/adminEdit')
def adminEdit():
    return render_template('adminEdit.html')

# dashboard routing 
@app.route('/dashboard')
def dashboard():
    data_list = []
    stmt = '''SELECT * FROM testdb'''
    cur = conn.cursor()
    cur.execute(stmt)
    cursor= cur.fetchall()
    for row in cursor:
    #   print(f"{row}")
      data_list.append(row)
    data = data_list

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('dashboard.html', labels=labels, values=values)

# courses route 
@app.route('/courses')
def courses():
    return render_template('courses.html')

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


if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)
