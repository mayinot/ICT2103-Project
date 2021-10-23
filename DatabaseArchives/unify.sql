-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: unify
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CategoryName` varchar(125) NOT NULL,
  `CategoryID` char(5) NOT NULL,
  `CategoryIcon` varchar(2048) NOT NULL,
  PRIMARY KEY (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `CourseName` varchar(125) NOT NULL,
  `CourseDesc` text NOT NULL,
  `CourseID` char(5) NOT NULL,
  `CourseURL` varchar(2048) NOT NULL,
  `AvgGradPay` float NOT NULL,
  `Intake` int NOT NULL,
  `UniName` varchar(125) NOT NULL,
  `FacultyID_` char(5) NOT NULL,
  PRIMARY KEY (`CourseID`),
  KEY `UniName` (`UniName`),
  KEY `FacultyID_` (`FacultyID_`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`UniName`) REFERENCES `university` (`UniName`),
  CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`FacultyID_`) REFERENCES `faculty` (`FacultyID_`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `FacultyID_` char(5) NOT NULL,
  `FacultyName` varchar(125) NOT NULL,
  `FacultyDesc` text NOT NULL,
  PRIMARY KEY (`FacultyID_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facultycategory`
--

DROP TABLE IF EXISTS `facultycategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facultycategory` (
  `FacultyID_` char(5) NOT NULL,
  `CategoryID` char(5) NOT NULL,
  PRIMARY KEY (`FacultyID_`,`CategoryID`),
  KEY `CategoryID` (`CategoryID`),
  CONSTRAINT `facultycategory_ibfk_1` FOREIGN KEY (`FacultyID_`) REFERENCES `faculty` (`FacultyID_`),
  CONSTRAINT `facultycategory_ibfk_2` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facultycategory`
--

LOCK TABLES `facultycategory` WRITE;
/*!40000 ALTER TABLE `facultycategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `facultycategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gradeprofile`
--

DROP TABLE IF EXISTS `gradeprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gradeprofile` (
  `Poly10thPerc` float NOT NULL,
  `Poly90thPerc` float NOT NULL,
  `Alevel90thPerc` varchar(20) NOT NULL,
  `Alevel10thPerc` varchar(20) NOT NULL,
  `CourseID` char(5) NOT NULL,
  PRIMARY KEY (`CourseID`),
  CONSTRAINT `gradeprofile_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `courses` (`CourseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gradeprofile`
--

LOCK TABLES `gradeprofile` WRITE;
/*!40000 ALTER TABLE `gradeprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `gradeprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `university`
--

DROP TABLE IF EXISTS `university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `university` (
  `UniName` varchar(125) NOT NULL,
  `UniAbb` varchar(10) NOT NULL,
  `UniDesc` text NOT NULL,
  `UniImage` varchar(2048) NOT NULL,
  PRIMARY KEY (`UniName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-18 23:54:17

