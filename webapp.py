from flask import Flask, render_template
from flask import request, redirect, url_for, flash
from db_connector import connect_to_database, execute_query
#create the web application
app = Flask(__name__)
app.secret_key = "SECRETKEY"

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/members')
def members():
	db_connection = connect_to_database()
	query = "SELECT m.first_name, m.last_name, m.birth_date, m.gender, m.weight, p.program_name, l.branch_name,\
	CONCAT_WS(' ', t.first_name, t.last_name) \
	FROM members m \
	INNER JOIN locations l ON m.preferred_location = l.location_id \
	LEFT JOIN programs p ON m.program_id = p.program_id \
	LEFT JOIN trainers t ON m.trainer_id = t.trainer_id;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('members.html',rows=result)

@app.route('/locations')
def locations():
	db_connection = connect_to_database()
	query = "SELECT branch_name, address_line1, address_line2, city, state, zip from locations;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('locations.html',rows=result)
	
@app.route('/trainers')
def trainers():
	db_connection = connect_to_database()
	query = "SELECT t.first_name, t.last_name, t.birth_date, t.gender, t.date_employed, t.capacity, l.branch_name, \
	GROUP_CONCAT(q.qual_name SEPARATOR', ') from trainers t \
	INNER JOIN locations l ON t.location_id = l.location_id \
	LEFT JOIN trainer_qualifications tq ON t.trainer_id = tq.trainer_id \
	LEFT JOIN qualifications q ON tq.qual_id = q.qual_id GROUP BY t.trainer_id;"
	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('trainers.html',rows=result)

@app.route('/qualifications')
def qualifications():
	db_connection = connect_to_database()
	query = "SELECT qual_name, is_cert from qualifications;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('qualifications.html',rows=result)

@app.route('/programs')
def programs():
	db_connection = connect_to_database()
	query = "SELECT program_name from programs;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('programs.html',rows=result)

@app.route('/addMember', methods=['POST','GET'])
def addMember():
	db_connection = connect_to_database()
	if request.method == 'GET':
		query1 = "SELECT program_id, program_name from programs;"
		result1 = execute_query(db_connection, query1).fetchall()
		query2 = "SELECT location_id, branch_name from locations;"
		result2 = execute_query(db_connection, query2).fetchall()
		query3 = "SELECT trainer_id, first_name, last_name from trainers;"
		result3 = execute_query(db_connection, query3).fetchall()
		return render_template('addMember.html', programs=result1, locations=result2, trainers=result3)
	elif request.method == 'POST':
		first_name_input = request.form['first_name']
		last_name_input = request.form['last_name']
		birth_date_input = request.form['birth_date']
		gender_input = request.form['gender']
		if gender_input == 'male':
			gender_input = 0
		elif gender_input == 'female':
			gender_input = 1
		else:
			gender_input = 2
		weight_input = request.form['weight']
		program_id_input = request.form['program_id']
		location_dropdown_input = request.form['preferred_location']
		trainer_id_dropdown_input = request.form['trainer_id']
		query1 = "INSERT INTO members (first_name, last_name, birth_date, gender, weight, program_id, preferred_location, trainer_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
		data1 = (first_name_input,last_name_input,birth_date_input,gender_input, weight_input, program_id_input, location_dropdown_input, trainer_id_dropdown_input)
		result1 = execute_query(db_connection, query1, data1)
		myMemberID = result1.lastrowid
		print("My Member ID:")
		print(myMemberID)
		flash(u'A Member Has Been Added!!', 'confirmation')
		return redirect(url_for('members'))

@app.route('/addLocation', methods=['POST','GET'])
def addLocation():
	if request.method == 'GET':
		return render_template('addLocation.html')
	elif request.method == 'POST':
		branch_name_input = request.form['branch_name']
		address_line1_input = request.form['address_line1']
		address_line2_input = request.form['address_line2']
		city_input = request.form['city']
		state_input = request.form['state']
		zip_input = request.form['zip']
		db_connection = connect_to_database()
		query = "INSERT INTO locations(branch_name, address_line1, address_line2, city, state, zip) VALUES (%s, %s,%s,%s,%s,%s)"
		data = (branch_name_input, address_line1_input, address_line2_input, city_input, state_input, zip_input)
		execute_query(db_connection, query, data)
		flash(u'A Location Has Been Added!!', 'confirmation')
		return redirect(url_for('locations'))
		
@app.route('/addTrainer',methods=['POST','GET'])
def addTrainer():
	db_connection = connect_to_database()
	if request.method == 'GET':
		query1 = "Select qual_id, qual_name from qualifications;"
		result1 = execute_query(db_connection, query1).fetchall()
		query2 = "SELECT location_id, branch_name from locations;"
		result2 = execute_query(db_connection, query2).fetchall()
		return render_template('addTrainer.html', quals=result1, locations=result2)
	elif request.method == 'POST':
		first_name_input = request.form['first_name']
		last_name_input = request.form['last_name']
		birth_date_input = request.form['birth_date']
		gender_input = request.form['gender']
		if gender_input == 'male':
			gender_input = 0
		elif gender_input == 'female':
			gender_input = 1
		else:
			gender_input = 2
		date_employed_input = request.form['date_employed']
		capacity_input = request.form['capacity']
		location_dropdown_input = request.form['location_id']
		qual_id_dropdown_input = request.form['qual_id']
		query1 = "INSERT INTO trainers (first_name, last_name, birth_date, gender, date_employed, capacity, location_id) \
		VALUES (%s,%s,%s,%s,%s,%s,%s)"
		data1 = (first_name_input,last_name_input,birth_date_input,gender_input,date_employed_input,capacity_input,location_dropdown_input)
		result1 = execute_query(db_connection, query1, data1)
		myTrainerID = result1.lastrowid
		print("My Trainer ID:")
		print(myTrainerID)
		query2="INSERT INTO trainer_qualifications (trainer_id, qual_id) VALUES (%s, %s)"
		data2= (myTrainerID,qual_id_dropdown_input)
		execute_query(db_connection, query2, data2)
		flash(u'A Trainer Has Been Added!!', 'confirmation')
		return redirect(url_for('trainers'))

@app.route('/addQualification',methods=['POST','GET'])
def addQualification():
	if request.method == 'GET':
		return render_template('addQualification.html')
	elif request.method == 'POST':
		qual_name_input = request.form['qual_name']
		is_cert_input = request.form['is_cert']
		if is_cert_input == 'yes':
			is_cert_input = 1
		else:
			is_cert_input = 0
		db_connection = connect_to_database()
		query = "INSERT INTO qualifications (qual_name, is_cert) VALUES (%s, %s)"
		data = (qual_name_input, is_cert_input)
		execute_query(db_connection, query, data)
		flash(u'A Qualification Has Been Added!!', 'confirmation')
		return redirect(url_for('qualifications'))

@app.route('/addProgram',methods=['POST','GET'])
def addProgram():
	if request.method == 'GET':
		return render_template('addProgram.html')
	elif request.method == 'POST':
		program_name_input = request.form['program_name']
		db_connection = connect_to_database()
		query = "INSERT INTO programs (program_name) VALUES (%s)"
		data = (program_name_input,)
		execute_query(db_connection, query, data)
		flash(u'A Program Has Been Added!!', 'confirmation')
		return redirect(url_for('programs'))

@app.route('/updateMember')
def updateMember():
	return render_template('updateMember.html')

@app.route('/updateTrainer',methods=['POST','GET'])
def updateTrainer():
	return render_template('updateTrainer.html')

@app.route('/updateLocation')
def updateLocation():
	return render_template('updateLocation.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)
