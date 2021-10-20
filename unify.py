from flask import Flask, render_template

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

if __name__ == "__main__":
    # Error will be displayed on web page 
    app.run(debug=True)
