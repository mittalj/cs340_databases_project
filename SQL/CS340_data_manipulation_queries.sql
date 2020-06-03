-- These are some Database Manipulation queries for a partially implemented Project Website
-- using the bsg database.
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.

-- Get all qualification data for the qualifications page
SELECT qual_name, is_cert from qualifications;

-- Get all program data for the programs page
SELECT program_name from programs;

-- Get all members data for the members page
SELECT m.first_name, m.last_name, m.birth_date, m.gender, m.weight, p.program_name, l.branch_name, CONCAT_WS(' ', t.first_name, t.last_name) FROM members m
INNER JOIN locations l ON m.preferred_location = l.location_id
LEFT JOIN programs p ON m.program_id = p.program_id
LEFT JOIN trainers t ON m.trainer_id = t.trainer_id;

-- Get all personal trainer data for the personal trainer page
-- https://stackoverflow.com/questions/24241953/sql-query-of-multiple-values-in-one-cell --
SELECT t.first_name, t.last_name, t.birth_date, t.gender, t.date_employed, t.capacity, l.branch_name,
GROUP_CONCAT(q.qual_name SEPARATOR', '), t.trainer_id from trainers t
INNER JOIN locations l ON t.location_id = l.location_id
LEFT JOIN trainer_qualifications tq ON t.trainer_id = tq.trainer_id
LEFT JOIN qualifications q ON tq.qual_id = q.qual_id
GROUP BY t.trainer_id;

-- Get all location data for the locations page
SELECT branch_name, address_line1, address_line2, city, state, zip from locations;

-- Add Member --
INSERT INTO members (first_name, last_name, birth_date, gender, weight, program_name, preferred_location)
VALUES (:first_name_input, :last_name_input, :birth_date_input, :gender_input, :weight_input, :program_name_dropdown_input, :preferred_location_dropdown_input);

-- Add Trainer --
INSERT INTO trainers (first_name, last_name, birth_date, gender, date_employed, capacity, location_id)
VALUES (:first_name_input, :last_name_input, :birth_date_input, :gender_input, :date_employed_input, :capacity_input, :location_input);
INSERT INTO trainer_qualifications (trainer_id, qual_id)
VALUES (:myTrainerID, :qual_id_dropdown_input);

-- Add Location --
INSERT INTO locations (branch_name, address_line1, address_line2, city, state, zip)
VALUES (:branch_name_input, :address_line1_input, :address_line2_input, :city_input, :state_input, :zip_input);

-- Add Program --
INSERT INTO programs (program_name)
VALUES (:program_name_input);

-- Add Qualification --
INSERT INTO qualifications (qual_name, is_cert)
VALUES (:qual_name_input, is_cert_input);

-- Update Members --
UPDATE members SET first_name = :first_name_input, last_name= :last_name_input, birth_date = :birth_date_input, gender= :gender_input, weight = :weight_input, program_name = :program_name_input, branch_name = :branch_name_input
WHERE member_id= :member_ID_from_the_update_form;

-- Update Personal Trainers
UPDATE trainers SET first_name = :first_name_input, last_name= :last_name_input, birth_date = :birth_date_input, gender= :gender_input, date_employed = :date_employed_input, capacity = :capacity_input, branch_name = :branch_name_input,
qual_name = :qual_name_input WHERE trainer_id= :trainer_ID_from_the_update_form;
UPDATE trainer_qualifications SET trainer_id = :trainer_id_input, qual_id = :qual_id_input WHERE trainer_id = :trainer_ID_selected_from_trainer_list AND qual_id = :trainer_qualification_ID_selected_from_qualification_list

-- Update Locations --
UPDATE locations SET branch_name = :branch_name_input, address_line1= :address_line1_input, address_line2 = :address_line2_input, city= :city_input, state = :state_input, zip = :zip_input WHERE location_id= :location_ID_from_the_update_form;

--Delete member--
DELETE FROM members WHERE member_id = :member_ID_selected_from_browse_member_page;

--Delete trainer--
DELETE FROM trainers WHERE trainer_id = :trainer_ID_selected_from_trainer_list;

-- Locations Dropdown --
SELECT location_id, branch_name from locations

-- Qualifications Dropdown --
Select qual_id, qual_name from qualifications

-- Personal Trainer Dropdown --
SELECT trainer_id, first_name, last_name FROM trainers

-- Programs Dropdown --
SELECT program_id, program_name from programs
