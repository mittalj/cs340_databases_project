from flask import Flask, render_template
from flask import request, redirect, url_for, flash
from db_connector import connect_to_database, execute_query
import collections
import itertools

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
	CONCAT_WS(' ', t.first_name, t.last_name), m.member_id \
	FROM members m \
	INNER JOIN locations l ON m.preferred_location = l.location_id \
	LEFT JOIN programs p ON m.program_id = p.program_id \
	LEFT JOIN trainers t ON m.trainer_id = t.trainer_id;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('members.html',rows=result)

@app.route('/locations')
def locations():
	db_connection = connect_to_database()
	query = "SELECT branch_name, address_line1, address_line2, city, state, zip, location_id from locations;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('locations.html',rows=result)

@app.route('/trainers')
def trainers():
	db_connection = connect_to_database()
	query = "SELECT t.first_name, t.last_name, t.birth_date, t.gender, t.date_employed, t.capacity, l.branch_name, \
	GROUP_CONCAT(q.qual_name SEPARATOR', '), t.trainer_id from trainers t \
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

@app.route('/getTrainer/<location_id>')
def getTrainer(location_id):
	db_connection = connect_to_database()
	query3 = "SELECT CONCAT_WS(' ', first_name, last_name) from trainers WHERE location_id = %s;" % (location_id)
	result3 = execute_query(db_connection, query3).fetchall()
	return jsonify(result3)

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

		if program_id_input == "":
			program_id_input = None

		if trainer_id_dropdown_input == "":
			trainer_id_dropdown_input = None

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
	# Populate data for dropdown fields on the template form
	if request.method == 'GET':
		query1 = "Select qual_id, qual_name from qualifications;"
		result1 = execute_query(db_connection, query1).fetchall()
		query2 = "SELECT location_id, branch_name from locations;"
		result2 = execute_query(db_connection, query2).fetchall()
		return render_template('addTrainer.html', quals=result1, locations=result2)
	# When form is submitted, get data from form fields and commit it to the database
	elif request.method == 'POST':
		# First insert a trainer record into the trainers table
		first_name_input = request.form['first_name']
		last_name_input = request.form['last_name']
		birth_date_input = request.form['birth_date']
		gender_input = request.form['gender']
		# Convert gender values to integers
		if gender_input == 'male':
			gender_input = 0
		elif gender_input == 'female':
			gender_input = 1
		else:
			gender_input = 2
		date_employed_input = request.form['date_employed']
		capacity_input = request.form['capacity']
		location_dropdown_input = request.form['location_id']
		query1 = "INSERT INTO trainers (first_name, last_name, birth_date, gender, date_employed, capacity, location_id) \
		VALUES (%s,%s,%s,%s,%s,%s,%s)"
		data1 = (first_name_input,last_name_input,birth_date_input,gender_input,date_employed_input,capacity_input,location_dropdown_input)
		result1 = execute_query(db_connection, query1, data1)
		# Get the value of the inserted trainer id
		myTrainerID = result1.lastrowid
		# Retreive qualification values from the form
		values = request.form.getlist('input_text')
		# Run a loop to insert a trainer qual record into the trainer_qualifications table
		for v in values:
			qual_id_dropdown_input = v
			query2="INSERT INTO trainer_qualifications (trainer_id, qual_id) VALUES (%s, %s)"
			data2= (myTrainerID,qual_id_dropdown_input)
			execute_query(db_connection, query2, data2)
		flash(u'A Trainer Has Been Added!!', 'confirmation')
		return redirect(url_for('trainers'))

@app.route('/addQualification',methods=['POST','GET'])
def addQualification():
	if request.method == 'GET':
		return render_template('addQualification.html')
	# When form is submitted, get data from form fields and commit it to the database
	elif request.method == 'POST':
		qual_name_input = request.form['qual_name']
		is_cert_input = request.form['is_cert']
		# Convert cert values to integers
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
	# When form is submitted, get data from form fields and commit it to the database
	elif request.method == 'POST':
		program_name_input = request.form['program_name']
		db_connection = connect_to_database()
		query = "INSERT INTO programs (program_name) VALUES (%s)"
		data = (program_name_input,)
		execute_query(db_connection, query, data)
		flash(u'A Program Has Been Added!!', 'confirmation')
		return redirect(url_for('programs'))

@app.route('/updateMember/<int:id>', methods=['POST','GET'])
def updateMember(id):
	print("In the function")
	db_connection = connect_to_database()
	if request.method=='GET':
		print('The GET Request')
		member_query = 'SELECT member_id, first_name, last_name, birth_date, gender, weight, program_id, preferred_location, trainer_id  FROM members WHERE member_id = %s' % id
		member_result = execute_query(db_connection, member_query).fetchone()

		if member_result == None:
			return "No such member found!"

		trainer_query = 'SELECT trainer_id, first_name, last_name FROM trainers'
		trainer_result = execute_query(db_connection, trainer_query).fetchall()

		location_query = 'SELECT location_id, branch_name FROM locations'
		location_result = execute_query(db_connection, location_query).fetchall()

		program_query = "SELECT program_id, program_name from programs"
		program_result = execute_query(db_connection, program_query).fetchall()

		print("Returning")
		flash(u'A Member Has Been Updated.', 'confirmation')
		return render_template('updateMember.html', member = member_result, trainers = trainer_result, locations = location_result, programs = program_result)

	elif request.method == 'POST':
		print('The POST request')
		member_id_input = request.form['id']
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

		if program_id_input == "":
			program_id_input = None

		if trainer_id_dropdown_input == "":
			trainer_id_dropdown_input = None

		query = "UPDATE members SET first_name = %s, last_name = %s, birth_date = %s, gender = %s, weight = %s, program_id = %s, preferred_location = %s, trainer_id = %s WHERE member_id = %s"
		data = (first_name_input, last_name_input, birth_date_input, gender_input, weight_input, program_id_input,
				 location_dropdown_input, trainer_id_dropdown_input, member_id_input)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")
		return redirect(url_for('members'))

@app.route('/updateTrainer/<int:id>',methods=['POST','GET'])
def updateTrainer(id):
	db_connection = connect_to_database()
	if request.method == 'GET':
		# Get data for the single trainer id that needs to be updated
		trainerQuery = "Select trainer_id, first_name, last_name, birth_date, gender, \
		date_employed, capacity, location_id from trainers where trainer_id = %s"  % (id)
		trainer_result = execute_query(db_connection, trainerQuery).fetchone()
		if trainer_result is None:
			return "No such trainer found!"

		# Pull data for all of the trainer qualifications
		qualQuery = "Select qual_id from trainer_qualifications where trainer_id = %s" % (id)
		qual_result = execute_query(db_connection, qualQuery).fetchall()

		# Pull data for the dropdown fields on the update form
		query1 = "Select qual_id, qual_name from qualifications;"
		result1 = execute_query(db_connection, query1).fetchall()
		query2 = "SELECT location_id, branch_name from locations;"
		result2 = execute_query(db_connection, query2).fetchall()
		return render_template('updateTrainer.html', quals=result1, locations=result2, trainer=trainer_result, trainerQuals=qual_result)
	# When the form is submitted, commit the updates into the database
	elif request.method == 'POST':
		# First update the trainer record in the trainers table
		print('The POST request')
		trainer_id_input = request.form['trainer_id']
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
		query1 = "UPDATE trainers SET first_name = %s, last_name = %s, birth_date = %s, gender = %s, date_employed = %s, capacity = %s, location_id = %s WHERE trainer_id = %s"
		data1 = (first_name_input, last_name_input, birth_date_input, gender_input, date_employed_input, capacity_input,
				 location_dropdown_input, trainer_id_input)
		result1 = execute_query(db_connection, query1, data1)

		# Delete existing trainer qual records first to make it easier to work with the dynamic fields for trainer qualifications
		query = "DELETE FROM trainer_qualifications WHERE trainer_id = %s"
		data = (id,)
		result = execute_query(db_connection, query, data)

		# Add trainer qualifications from the updated form
		values = request.form.getlist('input_text')
		# Run a loop to add each trainer qualification record into the database 
		for v in values:
			qual_id_dropdown_input = v
			query2="INSERT INTO trainer_qualifications (trainer_id, qual_id) VALUES (%s, %s)"
			data2= (id,qual_id_dropdown_input)
			execute_query(db_connection, query2, data2)

		flash(u'The Trainer Record has been Updated!!', 'confirmation')
		print(str(result.rowcount) + " row(s) updated")
		return redirect(url_for('trainers'))

@app.route('/updateLocation/<int:id>', methods=['POST','GET'])
def updateLocation(id):
	print("In the function")
	db_connection = connect_to_database()
	if request.method == 'GET':
		location_query = 'SELECT location_id, branch_name, address_line1, address_line2, city, state, zip from locations WHERE location_id = %s' % id
		location_result = execute_query(db_connection, location_query).fetchone()

		if location_result == None:
			return "No such location found!"

		print("Returning")
		return render_template('updateLocation.html', location = location_result)

	elif request.method == 'POST':
		print('The POST request')
		location_id_input = request.form['id']
		branch_name_input = request.form['branch_name']
		address_line1_input = request.form['address_line1']
		address_line2_input = request.form['address_line2']
		city_input = request.form['city']
		state_input = request.form['state']
		zip_input = request.form['zip']
		query = "UPDATE locations SET branch_name = %s, address_line1 = %s, address_line2 = %s, city = %s, state = %s, zip = %s WHERE location_id = %s"
		data = (branch_name_input, address_line1_input, address_line2_input, city_input, state_input, zip_input, location_id_input)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")
		flash(u'The Location Record has been Updated!!', 'confirmation')
		return redirect(url_for('locations'))

@app.route('/delete_trainer/<int:id>')
def delete_trainer(id):
	'''deletes a person with the given id'''
	db_connection = connect_to_database()
	query = "DELETE FROM trainers WHERE trainer_id = %s"
	data = (id,)
	result = execute_query(db_connection, query, data)
	flash(u'A Trainer Has Been Deleted.', 'confirmation')
	return redirect(url_for('trainers'))

@app.route('/search', methods=['POST', 'GET'])
def search():
	if request.method == 'GET':
		print("get request")
		return render_template('search.html')
	elif request.method == 'POST':
		print("post request")
		db_connection = connect_to_database()
		search_input = request.form['first_name']
		query = "SELECT m.first_name, m.last_name, m.birth_date, m.gender, m.weight, p.program_name, l.branch_name,\
		CONCAT_WS(' ', t.first_name, t.last_name), m.member_id \
		FROM members m \
		INNER JOIN locations l ON m.preferred_location = l.location_id \
		LEFT JOIN programs p ON m.program_id = p.program_id \
		LEFT JOIN trainers t ON m.trainer_id = t.trainer_id where m.first_name = %s OR m.last_name = %s;"
		data = (search_input,search_input)
		result = execute_query(db_connection, query, data)
		return render_template('search.html', rows=result)

@app.route('/deleteMember/<int:id>')
def deleteMember(id):
	db_connection = connect_to_database()
	query = "DELETE FROM members WHERE member_id = %s"
	data = (id,)
	result = execute_query(db_connection, query, data)
	flash(u'A Member Has Been Deleted.', 'confirmation')
	return redirect(url_for('members'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)
