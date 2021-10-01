from flask import Flask, render_template

# Set up our application (ref this file)
app = Flask(__name__)

# index route 
@app.route('/')
def index():
    return render_template('index.html')

# admin route
@app.route('/admin-only/login/')
def admin():
    return render_template('admin/admin.html')

if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)
