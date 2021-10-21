# ICT2103-Project
Database Management Project

## Setting Up
### Requirements:
1. Install MySQL Workbench, MySQL Server 
2. Pip 
3. Python 
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

## TODO
- Organise Working directory for repository 
- Plan app routes for flask frontend 
- Backend APIs, how to get data?? 

## Reference
1. [Web Application with Flask+PostgreSQL and deploy to heroku](https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc)
2. [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
3. [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)