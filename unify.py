from flask import Flask, render_template, url_for

# Set up our application (ref this file)
app = Flask(__name__)

# index route 
@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')
=======
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

>>>>>>> ffd2d8d9a6128df6009bb3b9f3be6e34b4f3bbc0

if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)
