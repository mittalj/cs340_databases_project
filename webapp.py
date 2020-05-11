from flask import Flask, render_template
from flask import request, redirect, url_for
#from db_connector.db_connector import connect_to_database, execute_query
#create the web application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/locations')
def locations():
    return render_template('locations.html')

@app.route('/trainers')
def trainers():
    return render_template('trainers.html')

@app.route('/qualifications')
def qualifications():
    return render_template('qualifications.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/addMember')
def addMember():
    return render_template('addMember.html')

@app.route('/addLocation')
def addLocation():
    return render_template('addLocation.html')

@app.route('/addTrainer')
def addTrainer():
    return render_template('addTrainer.html')

@app.route('/addQualification')
def addQualification():
    return render_template('addQualification.html')

@app.route('/addProgram')
def addProgram():
    return render_template('addProgram.html')

if __name__ == '__main__':
    app.run(debug=True)
