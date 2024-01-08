-- MySQL dump 10.13  Distrib 5.5.16, for Win64 (x86)
--
-- Host: localhost    Database: sae
-- ------------------------------------------------------
-- Server version	5.5.16

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
-- Table structure for table `channelrequests`
--

DROP TABLE IF EXISTS `channelrequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channelrequests` (
  `requestID` int(11) NOT NULL AUTO_INCREMENT,
  `channelID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`requestID`),
  KEY `channelID` (`channelID`),
  KEY `userID` (`userID`),
  CONSTRAINT `channelrequests_ibfk_1` FOREIGN KEY (`channelID`) REFERENCES `channels` (`channelID`),
  CONSTRAINT `channelrequests_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channelrequests`
--

LOCK TABLES `channelrequests` WRITE;
/*!40000 ALTER TABLE `channelrequests` DISABLE KEYS */;
/*!40000 ALTER TABLE `channelrequests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channels` (
  `channelID` int(11) NOT NULL AUTO_INCREMENT,
  `channel_name` varchar(255) NOT NULL,
  `need_accept` varchar(20) NOT NULL DEFAULT 'None',
  PRIMARY KEY (`channelID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (1,'Général','None'),(2,'Blabla','None'),(3,'Comptabilité','True'),(4,'Informatique','True'),(5,'Marketing','True');
/*!40000 ALTER TABLE `channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `senderID` int(11) NOT NULL,
  `receiverID` int(11) DEFAULT NULL,
  `channelID` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`messageID`),
  KEY `senderID` (`senderID`),
  KEY `receiverID` (`receiverID`),
  KEY `channelID` (`channelID`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`senderID`) REFERENCES `users` (`userID`),
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiverID`) REFERENCES `users` (`userID`),
  CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`channelID`) REFERENCES `channels` (`channelID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,8,NULL,1,'test','2023-12-28 21:08:31'),(2,8,NULL,1,'test','2023-12-28 21:38:58'),(3,13,NULL,1,'tata','2023-12-28 21:39:30'),(4,13,NULL,1,'tata','2023-12-28 21:41:03'),(5,13,NULL,1,'test','2023-12-28 21:43:14'),(6,8,NULL,1,'tes','2023-12-28 21:44:01'),(7,8,NULL,1,'test','2023-12-28 21:47:15'),(8,8,NULL,1,'test','2023-12-28 21:51:58'),(9,8,NULL,1,'test','2023-12-28 21:53:08'),(10,8,NULL,1,'test','2023-12-28 21:53:33'),(11,13,NULL,1,'vava','2023-12-28 21:53:42'),(12,8,NULL,1,'test','2023-12-28 21:54:08'),(13,8,NULL,2,'test','2023-12-28 21:57:02'),(14,13,8,NULL,'test','2023-12-30 13:23:34'),(15,13,NULL,1,'test','2023-12-30 13:25:14'),(16,13,NULL,1,'test','2023-12-30 13:40:41'),(17,8,NULL,1,'test','2023-12-30 13:40:57'),(18,13,NULL,1,'salut','2023-12-30 13:41:05'),(19,8,13,NULL,'test','2023-12-30 13:41:13'),(20,13,8,NULL,'salut toto','2023-12-30 13:41:21'),(21,13,NULL,1,'test','2023-12-30 13:42:37'),(22,13,8,NULL,'salut','2023-12-30 13:45:30'),(23,13,NULL,4,'test','2023-12-30 14:29:36'),(24,16,NULL,4,'test','2023-12-30 14:30:24');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'access',
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (8,'toto','toto','192.168.1.19','ban',NULL),(13,'tata','tata','192.168.1.19','kick','2024-01-01 18:43:35'),(14,'admin','admin','192.168.1.19','access',NULL),(16,'trtr','trtr','192.168.1.19','access',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-31 16:30:12
