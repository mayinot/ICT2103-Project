from flask import Flask, render_template, url_for

# Set up our application (ref this file)
app = Flask(__name__)

# index route 
@app.route('/')
def index():
    return render_template('index.html')

# courses route 
@app.route('/courses')
def courses():
    return render_template('courses.html')

if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)
