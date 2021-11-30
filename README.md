# ICT2103-Project
Database Management Project

## Setting Up
### Pre-requisite:
1. Python v3.6 and above (Make sure it’s in your system PATH environment variable)
2. PIP3 (Make sure it’s in your system PATH environment variable)
3. Visual Studio Code or any IDE 
4. Any web browser, preferably Google Chrome or Mozilla Firefox 

### Set up 
1. git clone the repository 
2. Set up virtual env with `python -m venv venv` on the terminal. IMPT MAKE SURE YOU ARE IN THE CORRECT REPO DIRECTORY WHEN CREATING
3. To activate the virtual environment type `venv\Scripts\activate.bat` in your terminal
4. Install the dependencies with `pip install -r requirements.txt`
5. Copy these 2 commands and execute it in your terminal
```
set FLASK_APP=unify
```
and 
```
set FLASK_ENV=development
```
6. Once all these are set up, you just run the and debug the program but typing `flask run` in the terminal
7. If you're using VSCode, you could press F5 to instantly debug the web application, you just have to set the debug environment as Flask (second last option) and change app.py to unify.py


## Reference
1. [Web Application with Flask+PostgreSQL and deploy to heroku](https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc)
2. [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)


This user manual is written and moderated by Project UNIFY
