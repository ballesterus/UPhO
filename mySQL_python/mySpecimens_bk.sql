-- MySQL dump 10.13  Distrib 5.6.20, for osx10.8 (x86_64)
--
-- Host: localhost    Database: mySpecimens
-- ------------------------------------------------------
-- Server version	5.6.20

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
-- Table structure for table `CollectionEvent`
--

DROP TABLE IF EXISTS `CollectionEvent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CollectionEvent` (
  `idCollectionEvent` int(11) NOT NULL AUTO_INCREMENT,
  `CollectionDate` date NOT NULL,
  `CollectionMethod` varchar(45) DEFAULT NULL,
  `Notes` text,
  `idLocality` int(11) NOT NULL,
  PRIMARY KEY (`idCollectionEvent`,`idLocality`),
  KEY `fk_CollectionEvent_Locality1_idx` (`idLocality`),
  CONSTRAINT `fk_CollectionEvent_Locality1` FOREIGN KEY (`idLocality`) REFERENCES `Locality` (`idLocality`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CollectionEvent`
--

LOCK TABLES `CollectionEvent` WRITE;
/*!40000 ALTER TABLE `CollectionEvent` DISABLE KEYS */;
INSERT INTO `CollectionEvent` VALUES (1,'2014-07-02','General collecting','Day',1),(2,'2014-07-02','General collecting','Day',2),(3,'2014-07-02','General collecting','Night',4),(4,'2014-07-03','general collecting','day',5),(5,'2014-07-03','general collecting','',6),(6,'2014-07-03','general collecting','Night',8),(7,'2014-07-04','general collecting','Day',10),(8,'2014-07-04','general collecting','Day',11),(9,'2014-07-05','general collecting','Day',14),(10,'2014-07-05','general collecting','Day',15),(11,'2014-07-05','general collecting','Night',16),(12,'2014-07-06','general collecting','Day',17),(13,'2014-07-06','general collecting','Day',18),(14,'2014-07-06','general collecting','Day',19),(15,'2014-07-06','general collecting','Night',20),(16,'2014-07-07','general collecting','Day',21),(17,'2014-07-07','general collecting','Day',23),(18,'2014-07-07','general collecting','Night',24),(19,'2014-07-08','general collecting','Day',25),(20,'2014-07-08','general collecting','Day',26),(21,'2014-07-08','general collecting','Day',27),(22,'2014-07-08','general collecting','Night',28),(23,'2014-07-09','general collecting','Day',29),(24,'2014-07-09','general collecting','Day',30),(25,'2014-07-09','general collecting','Day',31),(26,'2014-07-09','general collecting','Night',32),(27,'2014-07-10','general collecting','Day',33),(28,'2014-07-10','general collecting','Day',34),(29,'2014-07-10','general collecting','Day',35),(30,'2014-07-10','general collecting','Night',36),(31,'2014-07-11','general collecting','Day',37),(32,'2014-07-11','general collecting','Night',39),(33,'2014-07-12','gneral collecting','Day',40),(34,'2014-07-12','general collecting','Day',41),(35,'2014-07-12','general collecting','Day',42),(36,'2014-07-12','general collecting','Night',43),(37,'2014-07-13','general collecting','Day',44),(38,'2014-07-13','general collecting','Day',45),(39,'2014-07-13','general collecting','Day',46),(40,'2014-07-13','general collecting','Night',47),(41,'2014-07-14','general collecting','Day',48),(42,'2014-07-14','general collection','Day',49),(43,'2014-07-14','general collecting','Day',50),(44,'2014-07-14','general collecting','Night',51),(45,'2014-07-15','general collecting','Day',52),(46,'2014-07-15','general collecting','Day',53),(47,'2014-07-15','general collecting','Night',54),(48,'2014-07-16','general collecting','Day',55),(49,'2014-07-16','general collecting','Day',56),(50,'2014-07-16','general collecting','Night',57),(51,'2014-07-17','general collecting','Day',58),(52,'2014-07-17','general collecting','Night',60),(53,'2014-07-17','general collecting','Day',59),(54,'2014-07-18','general collecting','Day',61),(55,'2014-07-18','general collecting','Night',62),(56,'2014-07-19','general collecting','Day',63),(57,'2014-07-19','general collecting','Day',64),(58,'2014-07-19','general collecting','Day',65),(59,'2014-07-19','general collecting','Night',66),(60,'2014-07-20','general collecting','Day',67),(61,'2014-07-20','general collecting','Day',69),(62,'2014-07-20','general collecting','Day',71),(63,'2014-07-20','general collecting','Night',72),(64,'2014-07-21','general collecting','Night',74),(65,'2014-07-21','general collecting',' Day',75),(66,'2015-07-21','general collecting','Day',76),(67,'2014-07-21','general collecting','Day',77),(68,'2014-07-21','general collecting','Night',78),(69,'2014-07-22','general collecting','Day',79),(70,'2014-07-22','general collecting',' Day',80),(71,'2012-09-15','general collecting','N',88),(72,'2012-09-01','general collecting','',89),(73,'2012-08-26','general collecting','',90),(74,'2012-09-02','general collecting','NULL',91),(75,'2012-09-01','general collecting','',151),(76,'2002-04-23','','',92),(77,'2002-04-23','','',92),(78,'2012-08-23','','',93),(79,'2012-08-23','','',94),(80,'2012-08-21','','',95),(81,'2013-05-18','general collecting','',96),(82,'2013-05-13','general collecting','',97),(83,'2013-05-18','general collecting','',98),(84,'2013-07-11','general collecting','',106),(85,'2013-07-18','general collecting','',107),(86,'2013-07-12','general collecting','',108),(87,'2013-07-21','general collecting','',109),(88,'2013-07-12','genrl collecting','',110),(89,'2013-07-13','general collecting','',111),(90,'2013-07-16','general collecting','',112),(91,'2013-07-20','general collecting','',113),(92,'2013-07-14','general collecting','',114),(93,'2013-07-23','general collecting','',106),(94,'2013-07-19','general collecting','',115),(95,'2012-09-22','general collecting','Photo',90),(96,'2004-07-00','Sweep net','in field of long grasses',152),(97,'2004-07-00','','',153),(98,'2004-11-02','Rock rolling','',154),(99,'2004-07-00','','Under dead agave',155),(100,'2004-07-18','','around station and nearby river',156);
/*!40000 ALTER TABLE `CollectionEvent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Collectors`
--

DROP TABLE IF EXISTS `Collectors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Collectors` (
  `idCollectionEvent` int(11) NOT NULL,
  `idPersonel` int(11) NOT NULL,
  PRIMARY KEY (`idCollectionEvent`,`idPersonel`),
  KEY `fk_CollectionEvent_has_Personel_Personel1_idx` (`idPersonel`),
  KEY `fk_CollectionEvent_has_Personel_CollectionEvent1_idx` (`idCollectionEvent`),
  CONSTRAINT `fk_CollectionEvent_has_Personel_CollectionEvent1` FOREIGN KEY (`idCollectionEvent`) REFERENCES `CollectionEvent` (`idCollectionEvent`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_CollectionEvent_has_Personel_Personel1` FOREIGN KEY (`idPersonel`) REFERENCES `Personel` (`idPersonel`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Collectors`
--

LOCK TABLES `Collectors` WRITE;
/*!40000 ALTER TABLE `Collectors` DISABLE KEYS */;
INSERT INTO `Collectors` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(22,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),(30,1),(31,1),(32,1),(33,1),(34,1),(35,1),(36,1),(37,1),(38,1),(39,1),(40,1),(41,1),(42,1),(43,1),(44,1),(45,1),(46,1),(47,1),(48,1),(49,1),(50,1),(51,1),(52,1),(53,1),(54,1),(55,1),(56,1),(57,1),(58,1),(59,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1),(71,1),(72,1),(73,1),(74,1),(75,1),(81,1),(82,1),(84,1),(85,1),(86,1),(87,1),(88,1),(89,1),(90,1),(91,1),(92,1),(93,1),(94,1),(95,1),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),(16,2),(17,2),(18,2),(19,2),(20,2),(21,2),(22,2),(23,2),(24,2),(25,2),(26,2),(27,2),(28,2),(29,2),(30,2),(31,2),(32,2),(33,2),(34,2),(35,2),(36,2),(37,2),(38,2),(39,2),(40,2),(41,2),(42,2),(43,2),(44,2),(45,2),(46,2),(47,2),(48,2),(49,2),(50,2),(51,2),(52,2),(53,2),(54,2),(55,2),(56,2),(57,2),(58,2),(59,2),(60,2),(61,2),(62,2),(63,2),(64,2),(65,2),(66,2),(67,2),(68,2),(69,2),(70,2),(82,2),(84,4),(85,4),(86,4),(87,4),(88,4),(89,4),(90,4),(91,4),(92,4),(93,4),(94,4),(77,5),(78,6),(79,6),(80,7),(83,8),(96,9),(97,9),(99,9),(100,9),(98,10),(98,11),(98,12),(100,13);
/*!40000 ALTER TABLE `Collectors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Determination`
--

DROP TABLE IF EXISTS `Determination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Determination` (
  `idDetermination` int(11) NOT NULL AUTO_INCREMENT,
  `DetDate` date NOT NULL,
  `idSpecies` int(11) NOT NULL,
  `idPersonel` int(11) NOT NULL,
  PRIMARY KEY (`idDetermination`,`idSpecies`,`idPersonel`),
  KEY `fk_Determination_Species1_idx` (`idSpecies`),
  KEY `fk_Determination_Personel1_idx` (`idPersonel`),
  CONSTRAINT `fk_Determination_Personel1` FOREIGN KEY (`idPersonel`) REFERENCES `Personel` (`idPersonel`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_Determination_Species1` FOREIGN KEY (`idSpecies`) REFERENCES `Species` (`idSpecies`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Determination`
--

LOCK TABLES `Determination` WRITE;
/*!40000 ALTER TABLE `Determination` DISABLE KEYS */;
INSERT INTO `Determination` VALUES (1,'2014-08-00',1,1),(2,'2014-08-00',2,1),(3,'2012-09-00',1,1),(5,'2011-00-00',1,3),(6,'2013-12-00',1,1),(7,'2014-09-00',2,1),(8,'2014-09-00',3,1),(9,'2014-09-00',4,1);
/*!40000 ALTER TABLE `Determination` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locality`
--

DROP TABLE IF EXISTS `Locality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locality` (
  `idLocality` int(11) NOT NULL AUTO_INCREMENT,
  `LocalityName` text NOT NULL,
  `Country` varchar(45) NOT NULL,
  `State` varchar(45) DEFAULT NULL,
  `County` varchar(45) DEFAULT NULL,
  `DecimalLong` float DEFAULT NULL,
  `DecimalLat` float DEFAULT NULL,
  `Elevation` int(11) DEFAULT NULL,
  `Notes` text,
  PRIMARY KEY (`idLocality`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locality`
--

LOCK TABLES `Locality` WRITE;
/*!40000 ALTER TABLE `Locality` DISABLE KEYS */;
INSERT INTO `Locality` VALUES (1,'Columbia Furnace Church of the Brethren','USA','Virginia','Shenandoah County',-78.5948,38.8714,316,'Loc01'),(2,'Sterret Rd','USA','Virginia','Rockbridge County',-79.2989,37.9184,467,'Loc02'),(3,'Mountain Lake Biological Station','USA','Virginia','Giles County',-80.5221,37.375,1178,'Loc03'),(4,'Moonshine Dell Trails, Mountain Lake Biological Station','USA','Virginia','Giles County',-80.5186,37.3727,1187,'Loc04'),(5,'Mountain Evangelist Marker, KG15','USA','Virginia','Giles County',-80.708,37.2417,562,'Loc05'),(6,'nr. Mount Rogers National Recreation Area','USA','Virginia',' Wythe County',-81.0461,36.8334,658,'Loc06'),(7,'E Old US Highway 64, Lexington','USA','North Carolina','Davidson County',-80.1031,35.7324,232,'Loc07'),(8,'nr.  Arrowhead Campground, Uwharrie National Forest','USA','North Carolina','Montgomery County',-80.0713,35.4396,191,'Loc08'),(9,'nr. Pee Dee  National Wildlife Refuge','USA','North Carolina','Anson County',-80.0129,35.0709,107,'Loc09'),(10,'nr. Carolina SandHills National Wildlife Refuge','USA','South Carolina','Chesterfield County',-80.2219,34.5197,109,'Loc10'),(11,'nr. Santee State Park','USA','South Carolina','Orangeburg County',-80.4978,33.5472,47,'Loc11'),(12,'nr. Francis Marion National Forest','USA','South Carolina','Â Berkeley County',-79.8549,32.9604,39,'Loc12'),(13,'Edisto River Wildlife Management Area    ','USA','South Carolina','Colleton County',-80.4192,32.9659,7,'Loc13'),(14,'nr. Rivers Bridge State Park','USA','South Carolina','Bamberg County',-81.0991,33.0507,29,'Loc14'),(15,'nr. Magnolia Springs, State Park','USA','Georgia','Jenkins County',-81.9531,32.8853,65,'Loc15'),(16,'nr. Skidaway Island State Park','USA','Georgia','Chatham County',-81.0551,31.9422,6,'Loc16'),(17,'nr. Jekyll Island','USA','Georgia','Glynn County',-81.4155,31.1145,24,'Loc17'),(18,'nr. Osceola National Forest','USA','Florida','Baker County',-82.4417,30.2468,76,'Loc18'),(19,'Lake City Campground ','USA','Florida','Columbia County',-82.6364,30.2566,50,'Loc19'),(20,'nr. Big Shoals State Park','USA','Florida','Hamilton County',-82.6927,30.3512,42,'Loc20'),(21,'nr. San Felasco State Park','USA','Florida','Alachua County',-82.4732,29.7736,37,'Loc21'),(22,'nr. Silver Springs State Park','USA','Florida','Marion County',-82.0596,29.195,25,'Loc22'),(23,'nr. Lake Louisa State Park','USA','Florida','Lake County',-81.7446,28.4529,47,'Loc23'),(24,'Archbold Biological Station','USA','Florida','Highlands County',-81.3504,27.1818,56,'Loc24'),(25,'nr. Apoxee Trail','USA','Florida','Palm Beach County',-80.1509,26.7267,-2,'Loc25'),(26,'nr. Navy Wells Pineland Preserve','USA','Florida','Miami-Dade county',-80.5069,25.4397,7,'Loc26'),(27,'nr. Everglades National Park','USA','Florida','Miami-Dade county',-80.584,25.3953,3,'Loc27'),(28,'Lake Annie, ArchBold Biological Station','USA','Florida','Highlands County',-81.3491,27.2106,41,'Loc28'),(29,'nr. Lake Wales Ridge State Forest','USA','Florida','Polk County',-81.4652,27.76,42,'Loc29'),(30,'nr. Colt Creek State Park','USA','Florida','Polk County',-82.0413,28.2959,45,'Loc30'),(31,'nr. Goethe State Park','USA','Florida','Levy County',-82.6331,29.1805,11,'Loc31'),(32,'Otter Springs Campground','USA','Florida','Gilchrist County',-82.9415,29.6453,-5,'Loc32'),(33,'nr. Ecofina River State Park','USA','Florida','Taylor County',-83.9065,30.059,7,'Loc33'),(34,'nr. Bear Creek State Park','USA','Florida','Gadsden County',-84.6248,30.4756,39,'Loc34'),(35,'nr. Conecuh National Forest','USA','Alabama','Covington County',-86.5575,31.1169,99,'Loc35'),(36,'nr. Frank Jackson State Park','USA','Alabama','Covington County',-86.2752,31.2983,90,'Loc36'),(37,'nr. Little River State Park','USA','Alabama','Escambia County',-87.4853,31.2402,91,'Loc37'),(38,'nr. De Soto National Forest','USA','Mississippi','Harrison County',-88.9411,30.5525,40,'Loc38'),(39,'nr. Tickfaw State Park','USA','Louisiana','Livingston Parish',-90.637,30.3838,-3,'Loc39'),(40,'nr. Three Rivers Wildlfe Management Area','USA','Louisiana','Concordia Parish',-91.6461,31.0099,31,'Loc40'),(41,'Red River Wildlife Management Area (WMA)','USA','Louisiana','Concordia Parish',-91.6771,31.1949,18,'Loc41'),(42,'nr. St. Catherine Creek National Wildlife Refuge','USA','Mississippi','Adams County',-91.4514,31.4073,28,'Loc42'),(43,'nr. Homochitto National Forest','USA','Mississippi','Franklin County',-90.9891,31.4255,118,'Loc43'),(44,'nr. Tensas River National Wildlife Refuge','USA','Louisiana','Madison Parish',-91.2854,32.3072,39,'Loc44'),(45,'nr. D\'Arbonne National Wildlife Refuge','USA','Louisiana','Union Parish',-92.1887,32.6185,59,'Loc45'),(46,'Poison Creek','USA','Arkansas','Ouachita County',-93.0053,33.6391,109,'Loc46'),(47,'nr. Ouchita National Forest','USA','Arkansas','Garland County',-93.1782,34.6179,218,'Loc47'),(48,'nr. Pinnacle Mountain State Park','USA','Arkansas','Pulaski County',-92.4636,34.8468,79,'Loc48'),(49,'nr. Henry Gray Hurricane Lake WMA','USA','Arkansas','White County',-91.4756,35.2596,72,'Loc49'),(50,'nr. Corkwood Conservation Area','USA','Missouri','Butler County',-90.5313,36.557,106,'Loc50'),(51,'nr. Lake Wappapello State Park','USA','Missouri','Wayne County',-90.3354,36.9382,109,'Loc51'),(52,'Tennesse Welcome Center','USA','Tennessee','Dyer County',-89.4694,36.0701,138,'Loc52'),(53,'nr. Fort Pillow State Park','USA','Tennessee',' Lauderdale County',-89.8359,35.644,105,'Loc53'),(54,'Lake Chewalla Recreation Area, Holly Springs','USA','Mississippi','Marshall County',-89.3411,34.7311,123,'Loc54'),(55,'nr. Chickasaw State Park','USA','Tennessee','Hardeman County',-88.8823,35.3416,166,'Loc55'),(56,'nr. Natchez Trace State Park','USA','Tennessee','Henderson County',-88.2672,35.798,189,'Loc56'),(57,'Wrangler Camp, Land Between the Lakes National Recreation Area','USA','Kentucky','Trigg County',-88.0074,36.7357,139,'Loc57'),(58,'nr. Lake Malone State Park','USA','Kentucky','Muhlenberg County',-87.0371,37.0748,148,'Loc58'),(59,'nr. Mammoth Cave National Park','USA','Kentucky','Barren County',-86.057,37.1042,220,'Loc59'),(60,'nr. Green River Lake State Park','USA','Kentucky','Taylor County',-85.3191,37.2763,161,'Loc60'),(61,'Bourbon Iron Furnace','USA','Kentucky','Bath County',-83.7481,38.1144,208,'Loc61'),(62,'nr. Shawnee State Park','USA','Ohio','Scioto County',-83.1802,38.7268,236,'Loc62'),(63,'Hanging Rock Recreation Area','USA','Ohio','Lawrence County',-82.7133,38.5732,263,'Loc63'),(64,'West Virginia Welcome Center','USA','West Virginia','Putnam county',-81.9984,38.4487,235,'Loc64'),(65,'nr. Kanawha State Forest','USA','West Virginia','Kanawha County',-81.6557,38.2682,291,'Loc65'),(66,'nr. Cedar Creek State Park','USA','West Virginia','Gilmer County',-80.8707,38.8769,289,'Loc66'),(67,'nr. Stonewall Jackson Lake WMA','USA','West Virginia','Lewis County',-80.5111,38.9588,351,'Loc67'),(68,'nr. Audra State Park','USA','West Virginia','Upshur County',-80.0689,39.0399,522,'Loc68'),(69,'Pleasant Valley WMA','USA','West Virginia','Barbour County',-80.0481,39.2461,349,'Loc69'),(70,'nr. Cathedral State Park','USA','West Virginia','Preston County',-79.538,39.3277,775,'Loc70'),(71,'nr. Deep Creek Lake State Park','USA','Maryland','Garrett County',-79.2985,39.5143,793,'Loc71'),(72,'nr. New Germany State Park','USA','Maryland','Garrett County',-79.119,39.6334,805,'Loc72'),(73,'nr. Green Ridge State Forest','USA','Maryland','Allegany County',-78.4588,39.6697,217,'Loc73'),(74,'Western Maryland Rail Trail','USA','Maryland','Washington County',-78.0182,39.6249,137,'Loc74'),(75,'nr. Mont Alto State Park','USA','Pennsylvania','Franklin County',-77.5365,39.8386,323,'Loc75'),(76,'nr. Caledonia State Park','USA','Pennsylvania','Franklin County',-77.4779,39.9068,290,'Loc76'),(77,'nr. Gettysburgh Visitor Center','USA','Pennsylvania','Adams County',-77.2283,39.8135,176,'Loc77'),(78,'nr. Cunningham Falls State Park','USA','Maryland','Frederick County',-77.4684,39.63,396,'Loc78'),(79,'nr. Sugarloaf Mountain Natural Area','USA','Maryland','Frederick County',-77.3798,39.2638,170,'Loc79'),(80,'nr. Blackhill Regional Park','USA','Maryland','Montgomery County',-77.2959,39.1934,138,'Loc80'),(88,'nr. Rock Creek Park','USA','District of Columbia',NULL,-77.0498,38.9275,NULL,NULL),(89,'nr. River Trail, C & O Canal Bike Trail','USA','Maryland','Montgomery County',-77.2482,39.0014,NULL,NULL),(90,'nr. Capital Crescent Bike Trail','USA','District of Columbia',NULL,-77.1117,38.9309,NULL,NULL),(91,'nr. C & O Canal Bike Trail','USA','District of Columbia',NULL,-77.0728,38.9048,NULL,NULL),(92,'Davies Creek','USA','Virginia',NULL,NULL,NULL,NULL,NULL),(93,'1196 Penry Road, residence','USA','Ohio','Delaware County',-83.1,40.3333,293,NULL),(94,'3271 Horseshoe Road','USA','Ohio','Delaware County',-83.0365,40.34,NULL,NULL),(95,'Bluff Road','USA','Louisiana','Ascension Parish',NULL,NULL,NULL,NULL),(96,'nr. George Washington National Forest','USA','Virginia','Shenandoah County',-78.3229,38.9365,277,NULL),(97,'ca. Winkler Botanical Preserve','USA','Virginia','Fairfax County',-77.1207,38.8291,3,NULL),(98,'Scheaffer farms bike trail, Seneca Creek State Park','USA','Maryland',NULL,-77.3178,39.1324,NULL,NULL),(99,'Casa de Tomas Garrido, Villa Luz','Mexico','Tabasco','Tacotalpa',-92.7656,17.4456,86,NULL),(100,'Cascadas de Misol-Ha','Mexico','Chiapas','Salto de Agua',-91.9991,17.3914,267,NULL),(101,'Jardines de Plaza Acuario','Mexico','Veracruz-Llave','Veracruz',-96.1221,19.1863,6,NULL),(102,'Bosque de Tlalpan','Mexico','Distrito Federal',NULL,-99.1949,19.2955,2327,NULL),(103,'Patio de Dña. Margarita Avila','Mexico','Veracruz-Llave','Veracruz',-96.1275,19.1787,13,NULL),(104,'Centro Turistico Poza Azul','Mexico','Chiapas','Salto de Agua',-92.3537,17.5578,68,NULL),(105,'Playa Varadero','Mexico','Tabasco','Paraíso',-93.2245,18.438,18,NULL),(106,'Puc Puggy Campground, Paynes Prairie Preserve State Park','USA','Florida','Alachua County',-82.2953,29.526,52,NULL),(107,'Silver Lake Campground, Withlacochee State Preserve','USA','Florida','Hernando County',-82.2132,28.5771,13,NULL),(108,'University of Florida, Gainesville','USA','Florida','Alachua County',-82.349,29.6454,55,NULL),(109,'1.3 Km S Nobleton','USA','Florida','Hernando County',-82.2617,28.6329,28,NULL),(110,'Puggy Road, Paynes Prairie State Park','USA','Florida','Alachua County',-82.2941,29.5281,46,NULL),(111,'University of Florida, Gainesville','USA','Florida','Alachua County',-82.3525,29.643,20,NULL),(112,'Chacala Trail, Paynes Prairie Preserve State Park','USA','Florida','Alachua County',-82.2857,29.5317,41,NULL),(113,'Holder Mine Campground, Withlacoochee State Preserve','USA','Florida','Citrus County',-82.383,28.8,21,NULL),(114,'University of Florida, Gainesville','USA','Florida','Alachua County',-82.3609,29.6481,38,NULL),(115,'Ridge Manor Trailhead, Withlacoochee State Park','USA','Florida','Hernando County',-82.2163,28.5186,29,NULL),(116,'Orillas de la laguna El Espejo','Mexico','Tabasco','Centro',-92.9666,17.9803,14,NULL),(117,'Patio de Dña. Margarita Avila','Mexico','Veracruz-Llave','Veracruz',-96.1275,19.1787,13,NULL),(118,'Patio de Dña. Alba Castillo','Mexico','Veracruz-Llave','Las Choapas',-94.0921,17.9336,11,NULL),(119,'Jardines de Plaza Acuario','Mexico','Veracruz-Llave','Veracruz',-96.1221,19.1863,6,NULL),(151,'nr. C & O Canal Bike Trail','USA','Maryland','Montgomery County',-77.1598,38.9706,63,''),(152,'Hwy 4 near San Pedro de Macoris','Dominican Republic','','',-69.1617,18.2893,23,''),(153,'East of La Romana North of large sugar plantation','Dominican Republic','La Romana','',-68.5507,18.2944,63,'SITE JH4'),(154,'R. M. O.  San Cristobal 145 Km federal road 190 Mitla-Tehuantepec','Mexico','Oaxaca','',-95.9666,16.5355,1160,''),(155,'West of Bayahibe','Dominican Republic','La Altagracia','',-68.5507,18.2331,50,''),(156,'La Palma, reserva cientifica Ebano verde','Dominican Republic','La Vega','',-70.5431,18.0323,1098,'');
/*!40000 ALTER TABLE `Locality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Personel`
--

DROP TABLE IF EXISTS `Personel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Personel` (
  `idPersonel` int(11) NOT NULL AUTO_INCREMENT,
  `LastName` varchar(45) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `MiddleName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idPersonel`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Personel`
--

LOCK TABLES `Personel` WRITE;
/*!40000 ALTER TABLE `Personel` DISABLE KEYS */;
INSERT INTO `Personel` VALUES (1,'Ballesteros','Jesus','Alfonso'),(2,'Kallal','Robert','James'),(3,'Hormiga','Gustavo',''),(4,'Chavez','Estrella','Belen'),(5,'Alvarez Padilla','Fernando',''),(6,'Bradley','Richard',''),(7,'Parys','K.','A.'),(8,'Benavides','Ligia','Rosario'),(9,'Huff','Jeremy',''),(10,'Paredes','Ricardo',''),(11,'Francke','Oscar','Federico'),(12,'Villegas','Gabriel',''),(13,'Volschenk','E.','S.');
/*!40000 ALTER TABLE `Personel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Species`
--

DROP TABLE IF EXISTS `Species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Species` (
  `idSpecies` int(11) NOT NULL AUTO_INCREMENT,
  `Family` varchar(45) DEFAULT NULL,
  `Genus` varchar(45) DEFAULT NULL,
  `Species` varchar(45) DEFAULT NULL,
  `Author` varchar(45) DEFAULT NULL,
  `Notes` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idSpecies`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Species`
--

LOCK TABLES `Species` WRITE;
/*!40000 ALTER TABLE `Species` DISABLE KEYS */;
INSERT INTO `Species` VALUES (1,'Tetragnathidae','Leucauge','venusta','White, 1841',NULL),(2,'Tetragnathidae','Leucauge','argyra','(Walckenaer, 1841)',''),(3,'Tetragnathidae','Leucauge','mariana','(Taczanowski, 1881)',''),(4,'Tetragnathidae','Leucauge','regnyi','(Simon, 1897)',''),(5,'Tetragnathidae','Leucauge','celebesiana','Yaginuma, 1954','');
/*!40000 ALTER TABLE `Species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Specimen`
--

DROP TABLE IF EXISTS `Specimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Specimen` (
  `idSpecimen` int(11) NOT NULL AUTO_INCREMENT,
  `GH_Number` varchar(45) DEFAULT NULL,
  `Preparation_Type` varchar(45) DEFAULT NULL,
  `otherCatalogNumber` varchar(45) DEFAULT NULL,
  `femaleCount` int(11) DEFAULT NULL,
  `maleCount` int(11) DEFAULT NULL,
  `juvenilesCount` int(11) DEFAULT NULL,
  `subAdultMaleCount` int(11) DEFAULT NULL,
  `subAdultFemaleCount` int(11) DEFAULT NULL,
  `Notes` text,
  `idDetermination` int(11) DEFAULT NULL,
  `idCollectionEvent` int(11) NOT NULL,
  PRIMARY KEY (`idSpecimen`,`idCollectionEvent`),
  KEY `fk_Specimen_Determination1_idx` (`idDetermination`),
  KEY `fk_Specimen_CollectionEvent1_idx` (`idCollectionEvent`),
  CONSTRAINT `fk_Specimen_Determination1` FOREIGN KEY (`idDetermination`) REFERENCES `Determination` (`idDetermination`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Specimen`
--

LOCK TABLES `Specimen` WRITE;
/*!40000 ALTER TABLE `Specimen` DISABLE KEYS */;
INSERT INTO `Specimen` VALUES (1,'GH1479','etOH 96%','',2,0,0,0,0,NULL,1,1),(2,'GH1480','etOH 96%','',40,2,1,0,0,NULL,1,3),(3,'GH1481','etOH 96%','',6,1,0,0,0,NULL,1,4),(4,'GH1482','etOH 96%','',4,0,0,0,0,NULL,1,5),(5,'GH1483','etOH 96%','',10,1,0,0,0,NULL,1,6),(6,'GH1484','etOH 96%','',13,0,0,0,0,NULL,1,7),(7,'GH1485','etOH 96%','',6,0,0,0,0,NULL,1,8),(8,'GH1486','etOH 96%','',3,0,0,0,0,NULL,1,9),(9,'GH1487','etOH 96%','',13,0,0,0,0,NULL,1,10),(10,'GH1488','etOH 96%','',0,0,0,1,0,NULL,1,11),(11,'GH1489','etOH 96%','',1,0,6,0,0,NULL,1,12),(12,'GH1490','etOH 96%','',4,2,19,0,0,NULL,1,13),(13,'GH1491','etOH 96%','',1,0,0,0,0,NULL,1,14),(14,'GH1492','etOH 96%','',3,0,3,0,0,NULL,1,15),(15,'GH1493','etOH 96%','',20,20,20,0,0,NULL,1,16),(16,'GH1494','etOH 96%','',5,0,8,0,0,NULL,1,17),(17,'GH1495','etOH 96%','',0,0,2,0,0,NULL,1,18),(18,'GH1496','etOH 96%','',1,0,0,0,0,NULL,2,18),(19,'GH1497','etOH 96%','',0,0,3,0,0,NULL,2,19),(20,'GH1498','etOH 96%','',0,0,3,0,0,NULL,2,20),(21,'GH1499','etOH 96%','',1,0,1,0,0,NULL,2,21),(22,'GH1500','etOH 96%','',1,0,0,0,0,NULL,1,22),(23,'GH1501','etOH 96%','',1,1,7,0,1,NULL,2,22),(24,'GH1502','etOH 96%','',1,0,0,0,0,NULL,1,23),(25,'GH1503','etOH 96%','',3,0,7,0,0,NULL,1,24),(26,'GH1504','etOH 96%','',0,0,1,0,0,NULL,1,25),(27,'GH1505','etOH 96%','',5,0,7,0,2,NULL,1,26),(28,'GH1506','etOH 96%','',0,0,14,0,0,NULL,1,27),(29,'GH1507','etOH 96%','',1,0,0,0,0,NULL,1,29),(30,'GH1508','etOH 96%','',5,0,0,0,0,NULL,1,30),(31,'GH1509','etOH 96%','',1,0,0,0,0,NULL,1,31),(32,'GH1510','etOH 96%','',0,0,0,0,1,NULL,1,32),(33,'GH1511','etOH 96%','',0,0,6,0,0,NULL,1,33),(34,'GH1512','etOH 96%','',10,0,0,0,0,NULL,1,34),(35,'GH1513','etOH 96%','',5,0,4,0,0,NULL,1,35),(36,'GH1514','etOH 96%','',4,0,2,0,0,NULL,1,36),(37,'GH1515','etOH 96%','',0,0,1,0,0,NULL,1,37),(38,'GH1516','etOH 96%','',3,0,9,0,1,NULL,1,38),(39,'GH1517','etOH 96%','',18,0,0,0,0,NULL,1,39),(40,'GH1518','etOH 96%','',7,0,5,0,0,NULL,1,40),(41,'GH1519','etOH 96%','',2,0,4,0,1,NULL,1,41),(42,'GH1520','etOH 96%','',7,1,7,0,0,NULL,1,42),(43,'GH1521','etOH 96%','',1,0,1,0,0,NULL,1,43),(44,'GH1522','etOH 96%','',2,1,2,0,0,NULL,1,44),(45,'GH1523','etOH 96%','',2,0,0,0,0,NULL,1,45),(46,'GH1524','etOH 96%','',4,0,2,0,2,NULL,1,46),(47,'GH1525','etOH 96%','',5,0,1,0,0,NULL,1,47),(48,'GH1526','etOH 96%','',5,0,0,0,0,NULL,1,48),(49,'GH1527','etOH 96%','',7,0,0,0,0,NULL,1,49),(50,'GH1528','etOH 96%','',5,0,0,0,0,NULL,1,50),(51,'GH1529','etOH 96%','',12,0,0,0,0,NULL,1,51),(52,'GH1531','etOH 96%','',24,0,0,0,0,NULL,1,52),(53,'GH1530','etOH 96%','',3,0,0,0,0,NULL,1,53),(54,'GH1532','etOH96%','',5,0,0,0,0,NULL,1,54),(55,'GH1533','etOH 96%','',2,0,0,0,0,NULL,1,55),(56,'GH1534','etOH 96%','',2,0,0,0,0,NULL,1,56),(57,'GH1535','etOH 96%','',1,0,0,0,0,NULL,1,57),(58,'GH1536','etOH 96%','',2,0,0,0,0,NULL,1,58),(59,'GH1537','etOH 96%','',8,0,0,0,0,NULL,1,59),(60,'GH1538','etOH 96%','',4,0,0,0,0,NULL,1,60),(61,'GH1539','etOH 96%','',1,0,0,0,0,NULL,1,61),(62,'GH1540','etOH 96%','',10,0,0,0,0,NULL,1,62),(63,'GH1541','etOH 96%','',4,0,0,0,0,NULL,1,63),(64,'GH1542','etOH 96%','',6,0,0,0,0,NULL,1,64),(65,'GH1543','etOH 96%','',3,0,0,0,0,NULL,1,65),(66,'GH1544','etOH 96%','',1,0,0,0,0,NULL,1,66),(67,'GH1545','etOH 96%','',2,0,0,0,0,NULL,1,67),(68,'GH1546','etOH 96%','',8,0,0,0,0,NULL,1,68),(69,'GH1547','etOH 96%','',2,0,0,0,0,NULL,1,69),(70,'GH1548','etOH 96%','',7,0,0,0,0,NULL,1,70),(71,'GH1721','etOH 96%','JAB00001',5,0,0,0,0,'NULL',3,71),(72,'GH1722','etOH 96%','JAB00002',7,1,0,0,0,'NULL',3,72),(73,'GH1723','etOH 96%','JAB00003',10,0,1,0,0,'NULL',3,73),(74,'GH1724','etOH 96%','JAB00004',1,0,0,0,0,'NULL',3,74),(75,'GH1725','etOH 96%','JAB0005',7,0,1,1,0,' Duplicate specime record?',3,73),(76,'GH1726','etOH 96%','JAB00006',5,0,0,0,0,'',3,151),(77,'GH1726','etOH 96%','JAB00006',5,0,0,0,0,'',3,75),(78,'GH1727','etOH 96%','JAB0007',1,0,0,0,0,'',5,77),(79,'GH1728','etOH 96%','JAB00008',3,0,0,0,0,'',6,78),(80,'GH1729','etOH 96%','JAB00009',3,0,0,0,0,'',6,79),(81,'GH1730','etOH 96%','JAB00010',4,0,0,0,0,'',6,80),(82,'GH1731','etOH 96%','JAB00011',2,2,7,0,0,'',6,81),(83,'GH1732','etOH 96%','JAB00012',1,1,0,0,0,'',6,82),(84,'GH1733','etOH 96%','JAB00013',3,1,1,0,0,'',6,83),(85,'GH1734','etOH 96%','JAB00014',8,0,2,2,0,'0',6,84),(86,'GH1735','etOH 96%','JAB00015',10,6,7,0,0,'',6,85),(87,'GH1736','etOH 96%','JAB00016',15,1,14,0,3,'',6,86),(88,'GH1737','etOH 96%','JAB0017',9,1,8,0,0,'',6,87),(89,'GH1738','etOH 96%','JAB00018',6,1,11,0,5,'',6,88),(90,'GH1739','etOH 96%','JAB00019',12,1,7,0,0,'',6,89),(91,'GH1740','etOH 96%','JAB00020',13,2,1,2,2,'',6,90),(92,'GH1741','etOH 96%','JAB00021, JAB00022',99,0,0,0,0,'two vials',6,91),(93,'GH1742','etOH 96%','JAB00023',99,0,0,0,0,'',6,92),(94,'GH1743','etOH 96%','JAB00024',1,0,2,0,0,'',6,93),(95,'GH1744','etOH 96%','JAB00025, JAB00026',99,0,0,0,0,'two vials',6,94),(96,'GH1745','etOH 96%','JAB00027',1,0,0,0,0,'Photo',6,95),(97,'GH1747','etOH 96%','',2,0,2,0,0,'ATOL',7,96),(98,'GH1746','etOH 96%','',1,0,0,0,0,'ATOL',7,97),(99,'GH1748','etOH 96%','',1,0,0,0,0,'',8,98),(100,'GH1749','etOH 96%','',1,0,0,0,0,'ATOL',9,99),(101,'GH1750','etOH 96%','',2,0,0,0,0,'',9,100);
/*!40000 ALTER TABLE `Specimen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `collection_view`
--

DROP TABLE IF EXISTS `collection_view`;
/*!50001 DROP VIEW IF EXISTS `collection_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `collection_view` AS SELECT 
 1 AS `IdNum`,
 1 AS `CollectionDate`,
 1 AS `Country`,
 1 AS `State`,
 1 AS `LocalityName`,
 1 AS `Collected_by`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `determination_view`
--

DROP TABLE IF EXISTS `determination_view`;
/*!50001 DROP VIEW IF EXISTS `determination_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `determination_view` AS SELECT 
 1 AS `iddetermination`,
 1 AS `DetDate`,
 1 AS `Binomen`,
 1 AS `Determined_by`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `specimen_view`
--

DROP TABLE IF EXISTS `specimen_view`;
/*!50001 DROP VIEW IF EXISTS `specimen_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `specimen_view` AS SELECT 
 1 AS `idSpecimen`,
 1 AS `GH_Number`,
 1 AS `Species_name`,
 1 AS `Amount`,
 1 AS `collectionDate`,
 1 AS `Geography`,
 1 AS `LocalityName`,
 1 AS `DecimalLong`,
 1 AS `DecimalLat`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `collection_view`
--

/*!50001 DROP VIEW IF EXISTS `collection_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `collection_view` AS select `collectionevent`.`idCollectionEvent` AS `IdNum`,cast(`collectionevent`.`CollectionDate` as char charset utf8) AS `CollectionDate`,`locality`.`Country` AS `Country`,`locality`.`State` AS `State`,`locality`.`LocalityName` AS `LocalityName`,group_concat(`personel`.`LastName` separator ', ') AS `Collected_by` from (((`collectionevent` join `locality` on((`collectionevent`.`idLocality` = `locality`.`idLocality`))) join `collectors` on((`collectors`.`idCollectionEvent` = `collectionevent`.`idCollectionEvent`))) join `personel` on((`collectors`.`idPersonel` = `personel`.`idPersonel`))) group by `IdNum` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `determination_view`
--

/*!50001 DROP VIEW IF EXISTS `determination_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `determination_view` AS select `determination`.`idDetermination` AS `iddetermination`,cast(`determination`.`DetDate` as char charset utf8) AS `DetDate`,concat_ws(' ',`species`.`Genus`,`species`.`Species`,`species`.`Author`) AS `Binomen`,`personel`.`LastName` AS `Determined_by` from ((`determination` join `species` on((`determination`.`idSpecies` = `species`.`idSpecies`))) join `personel` on((`determination`.`idPersonel` = `personel`.`idPersonel`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `specimen_view`
--

/*!50001 DROP VIEW IF EXISTS `specimen_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `specimen_view` AS select `specimen`.`idSpecimen` AS `idSpecimen`,`specimen`.`GH_Number` AS `GH_Number`,concat_ws(' ',`species`.`Genus`,`species`.`Species`) AS `Species_name`,((((`specimen`.`femaleCount` + `specimen`.`maleCount`) + `specimen`.`subAdultMaleCount`) + `specimen`.`subAdultFemaleCount`) + `specimen`.`juvenilesCount`) AS `Amount`,`collectionevent`.`CollectionDate` AS `collectionDate`,concat_ws(': ',`locality`.`Country`,`locality`.`State`) AS `Geography`,`locality`.`LocalityName` AS `LocalityName`,`locality`.`DecimalLong` AS `DecimalLong`,`locality`.`DecimalLat` AS `DecimalLat` from ((((`specimen` join `determination` on((`specimen`.`idDetermination` = `determination`.`idDetermination`))) join `species` on((`determination`.`idSpecies` = `species`.`idSpecies`))) join `collectionevent` on((`specimen`.`idCollectionEvent` = `collectionevent`.`idCollectionEvent`))) join `locality` on((`collectionevent`.`idLocality` = `locality`.`idLocality`))) order by `specimen`.`GH_Number` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-02 16:16:14
