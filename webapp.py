from flask import Flask, render_template
from flask import request, redirect, url_for
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

@app.route('/updateMember')
def updateMember():
    return render_template('updateMember.html')

@app.route('/updateTrainer')
def updateTrainer():
    return render_template('updateTrainer.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
