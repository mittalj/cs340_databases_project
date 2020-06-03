-- CS 340 Database Project- Group 29

-- ------------------------------------------------------
-- Server version	5.1.65-community-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs` (
  `program_id` int(11) NOT NULL AUTO_INCREMENT,
  `program_name` varchar(255) NOT NULL,
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `programs` WRITE;
/*!40000 ALTER TABLE `programs` DISABLE KEYS */;
INSERT INTO `programs` (program_name) 
VALUES 
('Yoga'),
('Pilates'),
('Weight Loss'),
('Cardio'),
('Body Fit');
/*!40000 ALTER TABLE `programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualifications`
--

DROP TABLE IF EXISTS `qualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qualifications` (
  `qual_id` int(11) NOT NULL AUTO_INCREMENT,
  `qual_name` varchar(255) NOT NULL,
  `is_cert` boolean NOT NULL,
  PRIMARY KEY (`qual_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `qualifications` WRITE;
/*!40000 ALTER TABLE `qualifications` DISABLE KEYS */;
INSERT INTO `qualifications` (qual_name, is_cert)
VALUES 
('Personal Training', 1),
('Strength Training', 0),
('Aerobics', 1),
('Weight Loss', 0),
('Pilates', 1);
/*!40000 ALTER TABLE `qualifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(255) NOT NULL,
  `address_line1` varchar(255) NOT NULL,
  `address_line2` varchar(255),
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` int(11) NOT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` (branch_name, address_line1, address_line2, city, state, zip) 
VALUES
('Hogwarts School', '180 Gryffindor Avenue', 'Unit 934', 'Beverly Hills', 'CA', 90210),
('Knockturn Alley', '100 Slytherin Court', 'Unit 20', 'Portland', 'OR', 97204),
('Ravenclaw Tower', '80 Ravenclaw Circle', NULL, 'Seattle', 'WA', 98101),
('Hufflepuff Commons', '70 Hufflepuff Road', 'Unit 30', 'New York City', 'NY', 10001),
('Diagon Alley Main', '60 Diagon Alley Avenue', NULL, 'Los Angeles', 'CA', 90001);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainers`
--

DROP TABLE IF EXISTS `trainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trainers` (
  `trainer_id` int(11) NOT NULL AUTO_INCREMENT,
  `location_id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `birth_date` date NOT NULL,
  `gender` tinyint NOT NULL,
  `date_employed` date NOT NULL,  
  `capacity` int(11) NOT NULL,
  PRIMARY KEY (`trainer_id`),
  CONSTRAINT `trainers_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `trainers` WRITE;
/*!40000 ALTER TABLE `trainers` DISABLE KEYS */;
INSERT INTO `trainers` (location_id, first_name, last_name, birth_date, gender, date_employed, capacity) 
VALUES 
(1, 'Rubeus', 'Hagrid', '1950-07-31', 0, '2019-08-21', 5),
(1, 'Albus', 'Dumbledore', '1940-07-31', 0, '2020-01-21', 7),
(2, 'Minerva', 'McGonagall', '1970-11-29', 1, '2019-02-08', 8),
(3, 'Severus', 'Snape', '1950-09-41', 0, '2019-05-02', 4),
(4, 'Horace', 'Slughorn', '1980-02-01', 0, '2018-08-22', 2);
/*!40000 ALTER TABLE `trainers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `members` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `trainer_id` int(11) DEFAULT NULL,
  `program_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `birth_date` date NOT NULL,
  `gender` tinyint NOT NULL,
  `weight` float(5,2) NOT NULL,  
  `preferred_location` int(11) NOT NULL,
  PRIMARY KEY (`member_id`),
  CONSTRAINT `members_ibfk_1` FOREIGN KEY (`trainer_id`) REFERENCES `trainers` (`trainer_id`) ON DELETE SET NULL, 
  CONSTRAINT `members_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `programs` (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` (trainer_id, program_id, first_name, last_name, birth_date, gender, weight, preferred_location) 
VALUES 
(1, 2, 'Harry', 'Potter', '1980-07-31', 0, 140, 2),
(2, 3, 'Ron', 'Weasley', '1980-03-01', 0, 160, 3),
(1, 3, 'Hermonie', 'Granger', '1979-09-19', 1, 120, 1),
(3, 1, 'Luna', 'Lovegood', '1981-02-13', 1, 125, 4),
(4, 4, 'Draco', 'Malfoy', '1980-06-05', 0, 140, 4);
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainer_qualifications`
--

DROP TABLE IF EXISTS `trainer_qualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trainer_qualifications` (
  `trainer_id` int(11) NOT NULL,
  `qual_id` int(11) NOT NULL,
  PRIMARY KEY (`trainer_id`,`qual_id`),
  CONSTRAINT `trainerqual_ibfk_1` FOREIGN KEY (`trainer_id`) REFERENCES `trainers` (`trainer_id`) ON DELETE CASCADE,
  CONSTRAINT `trainerqual_ibfk_2` FOREIGN KEY (`qual_id`) REFERENCES `qualifications` (`qual_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `trainer_qualifications` WRITE;
/*!40000 ALTER TABLE `trainer_qualifications` DISABLE KEYS */;
INSERT INTO `trainer_qualifications` (trainer_id, qual_id) 
VALUES 
(1, 2),
(1, 3),
(2, 2),
(3, 4),
(4, 5);
/*!40000 ALTER TABLE `trainer_qualifications` ENABLE KEYS */;
UNLOCK TABLES;
-- ------------------------------------------------------------------------------------------------------------

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-02-04 12:54:40
