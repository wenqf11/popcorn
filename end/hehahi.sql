/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.6.10 : Database - devicemgtdb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`devicemgtdb` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `devicemgtdb`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add k_class',8,'add_k_class'),(23,'Can change k_class',8,'change_k_class'),(24,'Can delete k_class',8,'delete_k_class'),(25,'Can add k_purview',9,'add_k_purview'),(26,'Can change k_purview',9,'change_k_purview'),(27,'Can delete k_purview',9,'delete_k_purview'),(28,'Can add k_role',10,'add_k_role'),(29,'Can change k_role',10,'change_k_role'),(30,'Can delete k_role',10,'delete_k_role'),(31,'Can add k_classrole',11,'add_k_classrole'),(32,'Can change k_classrole',11,'change_k_classrole'),(33,'Can delete k_classrole',11,'delete_k_classrole'),(34,'Can add k_user',12,'add_k_user'),(35,'Can change k_user',12,'change_k_user'),(36,'Can delete k_user',12,'delete_k_user'),(37,'Can add k_devicetype',13,'add_k_devicetype'),(38,'Can change k_devicetype',13,'change_k_devicetype'),(39,'Can delete k_devicetype',13,'delete_k_devicetype'),(40,'Can add k_supplier',14,'add_k_supplier'),(41,'Can change k_supplier',14,'change_k_supplier'),(42,'Can delete k_supplier',14,'delete_k_supplier'),(43,'Can add k_producer',15,'add_k_producer'),(44,'Can change k_producer',15,'change_k_producer'),(45,'Can delete k_producer',15,'delete_k_producer'),(46,'Can add k_spare',16,'add_k_spare'),(47,'Can change k_spare',16,'change_k_spare'),(48,'Can delete k_spare',16,'delete_k_spare'),(49,'Can add k_device',17,'add_k_device'),(50,'Can change k_device',17,'change_k_device'),(51,'Can delete k_device',17,'delete_k_device'),(52,'Can add k_form',18,'add_k_form'),(53,'Can change k_form',18,'change_k_form'),(54,'Can delete k_form',18,'delete_k_form'),(55,'Can add k_formitem',19,'add_k_formitem'),(56,'Can change k_formitem',19,'change_k_formitem'),(57,'Can delete k_formitem',19,'delete_k_formitem'),(58,'Can add k_route',20,'add_k_route'),(59,'Can change k_route',20,'change_k_route'),(60,'Can delete k_route',20,'delete_k_route'),(61,'Can add k_meter',21,'add_k_meter'),(62,'Can change k_meter',21,'change_k_meter'),(63,'Can delete k_meter',21,'delete_k_meter'),(64,'Can add k_maintenance',22,'add_k_maintenance'),(65,'Can change k_maintenance',22,'change_k_maintenance'),(66,'Can delete k_maintenance',22,'delete_k_maintenance'),(67,'Can add k_task',23,'add_k_task'),(68,'Can change k_task',23,'change_k_task'),(69,'Can delete k_task',23,'delete_k_task'),(70,'Can add k_taskitem',24,'add_k_taskitem'),(71,'Can change k_taskitem',24,'change_k_taskitem'),(72,'Can delete k_taskitem',24,'delete_k_taskitem'),(73,'Can add k_sparebill',25,'add_k_sparebill'),(74,'Can change k_sparebill',25,'change_k_sparebill'),(75,'Can delete k_sparebill',25,'delete_k_sparebill'),(76,'Can add k_sparecount',26,'add_k_sparecount'),(77,'Can change k_sparecount',26,'change_k_sparecount'),(78,'Can delete k_sparecount',26,'delete_k_sparecount'),(79,'Can add k_tool',27,'add_k_tool'),(80,'Can change k_tool',27,'change_k_tool'),(81,'Can delete k_tool',27,'delete_k_tool'),(82,'Can add k_tooluse',28,'add_k_tooluse'),(83,'Can change k_tooluse',28,'change_k_tooluse'),(84,'Can delete k_tooluse',28,'delete_k_tooluse'),(85,'Can add k_toolcount',29,'add_k_toolcount'),(86,'Can change k_toolcount',29,'change_k_toolcount'),(87,'Can delete k_toolcount',29,'delete_k_toolcount'),(88,'Can add k_project',30,'add_k_project'),(89,'Can change k_project',30,'change_k_project'),(90,'Can delete k_project',30,'delete_k_project'),(91,'Can add k_schedule',31,'add_k_schedule'),(92,'Can change k_schedule',31,'change_k_schedule'),(93,'Can delete k_schedule',31,'delete_k_schedule'),(94,'Can add k_staffworkinfo',32,'add_k_staffworkinfo'),(95,'Can change k_staffworkinfo',32,'change_k_staffworkinfo'),(96,'Can delete k_staffworkinfo',32,'delete_k_staffworkinfo'),(97,'Can add k_staffscoreinfo',33,'add_k_staffscoreinfo'),(98,'Can change k_staffscoreinfo',33,'change_k_staffscoreinfo'),(99,'Can delete k_staffscoreinfo',33,'delete_k_staffscoreinfo'),(100,'Can add k_staffegginfo',34,'add_k_staffegginfo'),(101,'Can change k_staffegginfo',34,'change_k_staffegginfo'),(102,'Can delete k_staffegginfo',34,'delete_k_staffegginfo'),(103,'Can add k_feedback',35,'add_k_feedback'),(104,'Can change k_feedback',35,'change_k_feedback'),(105,'Can delete k_feedback',35,'delete_k_feedback'),(106,'Can add k_deviceplan',36,'add_k_deviceplan'),(107,'Can change k_deviceplan',36,'change_k_deviceplan'),(108,'Can delete k_deviceplan',36,'delete_k_deviceplan'),(109,'Can add k_config',37,'add_k_config'),(110,'Can change k_config',37,'change_k_config'),(111,'Can delete k_config',37,'delete_k_config');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values (1,'pbkdf2_sha256$12000$uZvi0CMdVTtZ$KV4AYQ790cmuDXN7ktWaiEy5zcISUgHIR9ID+Od6jdo=','2015-07-31 06:18:09',1,'hahehi','','','hhyysbg@163.com',1,1,'2015-04-12 13:44:28'),(2,'pbkdf2_sha256$10000$fPkfeuFWOm7Q$mRRgi1LIiStJXdXye76dm3yfHlCnXlL+TrN7vjmRQ+0=','2015-05-01 07:09:01',0,'test1','','','',0,1,'2015-05-01 07:09:01'),(3,'pbkdf2_sha256$10000$R5fRnnAB92qP$8kGYC+W8/XszspeA+nTsqkYjA6gTj4TfImMlqKKYW2w=','2015-05-01 08:24:07',0,'user1','','','',0,1,'2015-05-01 08:24:07'),(4,'pbkdf2_sha256$10000$N7LQP7QhVHm8$ws8tLd5n09/pIGLqx8s5m2B/D6OBNEDvlIC9xJgtbkM=','2015-05-01 08:25:37',0,'user2','','','',0,1,'2015-05-01 08:25:37'),(5,'pbkdf2_sha256$10000$bzbxw7d6Zwt3$yqLH7e75JDMQWZEUpMVxyeIbxTz3jY3Ku4lfXBE+dnA=','2015-05-01 08:35:40',0,'user3','','','',0,1,'2015-05-01 08:35:40'),(6,'pbkdf2_sha256$10000$8fCR4xNap1N3$aCEUSvEGNcrfyTiIIMKf1ZeYl16M+gOG4uU3FboC5u0=','2015-05-01 09:18:27',0,'user4','','','',0,1,'2015-05-01 09:18:27'),(9,'pbkdf2_sha256$12000$Q1bhiangj3Sx$HeRObo51+SZE0EFOhioecWjxEUE7ZPfby1XIRB8Mdgk=','2015-07-20 12:34:49',0,'wenqingfu','','','thssvince@163.com',0,1,'2015-07-20 12:34:49'),(10,'pbkdf2_sha256$10000$VfnwFJ0hGOF3$ReKdqCqNX6D2g9DKURmbkazXwMsDaEP7CfEJQx1d+Hw=','2015-08-07 16:27:04',0,'lxf','','','1',0,1,'2015-08-07 16:27:04');

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `devicemgt_k_class` */

DROP TABLE IF EXISTS `devicemgt_k_class`;

CREATE TABLE `devicemgt_k_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentid` int(10) unsigned NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `depthname` varchar(50) NOT NULL,
  `name` varchar(30) NOT NULL,
  `code` varchar(5) NOT NULL,
  `logo` varchar(30) NOT NULL,
  `address` varchar(80) NOT NULL,
  `zipcode` varchar(30) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `license` varchar(30) NOT NULL,
  `licensetype` varchar(30) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_class` */

insert  into `devicemgt_k_class`(`id`,`parentid`,`depth`,`depthname`,`name`,`code`,`logo`,`address`,`zipcode`,`phone`,`license`,`licensetype`,`content`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,0,0,'company','WDYK company','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(2,1,1,'department','north dept','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(3,1,1,'department','south dept','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(4,1,1,'department','east_dept','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(5,2,2,'group','north_leader','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(6,2,2,'group','north_leader2','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(7,3,2,'group','south_leader','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(8,3,3,'group','south_leader2','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(9,4,2,'','east_leader1','','','','','','','','','',1,'2015-05-27',1,'2015-05-27',0,'2015-05-27','0'),(10,9,3,'','test','','','','','','','','','',1,'2015-05-27',1,'2015-05-27',0,'2015-05-27','0'),(11,1,1,'','test2','','','','','','','','','',1,'2015-05-28',1,'2015-05-28',0,'2015-05-28','0'),(12,1,1,'','微谷项目部','1','1','1','1','1','1','','','',1,'2015-08-08',1,'2015-08-08',0,'2015-08-08','0');

/*Table structure for table `devicemgt_k_classrole` */

DROP TABLE IF EXISTS `devicemgt_k_classrole`;

CREATE TABLE `devicemgt_k_classrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `roleid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_classrole_432947aa` (`classid_id`),
  KEY `devicemgt_k_classrole_a1a2a495` (`roleid_id`),
  CONSTRAINT `classid_id_refs_id_08bcb693` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `roleid_id_refs_id_74e15c3a` FOREIGN KEY (`roleid_id`) REFERENCES `devicemgt_k_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_classrole` */

/*Table structure for table `devicemgt_k_config` */

DROP TABLE IF EXISTS `devicemgt_k_config`;

CREATE TABLE `devicemgt_k_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eggbonus` double NOT NULL,
  `eggprobability` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_config` */

insert  into `devicemgt_k_config`(`id`,`eggbonus`,`eggprobability`) values (1,20,0.1);

/*Table structure for table `devicemgt_k_device` */

DROP TABLE IF EXISTS `devicemgt_k_device`;

CREATE TABLE `devicemgt_k_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `brand` varchar(30) NOT NULL,
  `producerid_id` int(11) NOT NULL,
  `typeid_id` int(11) NOT NULL,
  `supplierid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `name` varchar(30) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `serial` varchar(80) NOT NULL,
  `model` varchar(30) NOT NULL,
  `buytime` date NOT NULL,
  `content` varchar(200) NOT NULL,
  `qrcode` varchar(625) NOT NULL,
  `position` varchar(80) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  `lastmaintenance` date DEFAULT NULL,
  `nextmaintenance` date DEFAULT NULL,
  `maintenanceperiod` int(10) unsigned NOT NULL,
  `lastrepaire` date DEFAULT NULL,
  `lastmeter` date DEFAULT NULL,
  `notice` varchar(100) NOT NULL,
  `ownerid` int(10) unsigned NOT NULL,
  `spare` varchar(500) NOT NULL,
  `statelog` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_device_432947aa` (`classid_id`),
  KEY `devicemgt_k_device_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_device_3f5d477e` (`typeid_id`),
  KEY `devicemgt_k_device_69308dea` (`supplierid_id`),
  CONSTRAINT `classid_id_refs_id_e8134469` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_0ca0a6d9` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_b397bc4d` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`),
  CONSTRAINT `typeid_id_refs_id_33dcc1e6` FOREIGN KEY (`typeid_id`) REFERENCES `devicemgt_k_devicetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_device` */

insert  into `devicemgt_k_device`(`id`,`classid_id`,`brand`,`producerid_id`,`typeid_id`,`supplierid_id`,`state`,`name`,`brief`,`serial`,`model`,`buytime`,`content`,`qrcode`,`position`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`,`lastmaintenance`,`nextmaintenance`,`maintenanceperiod`,`lastrepaire`,`lastmeter`,`notice`,`ownerid`,`spare`,`statelog`) values (1,1,'brand1',1,1,1,'0','nwd052813','wd052813','aadfsdf','1231ccds','2015-07-07','','','sdsds','',0,'2015-05-31',1,'2015-06-01',0,'2015-06-01','',NULL,NULL,0,NULL,NULL,'',2,'',''),(2,1,'new brand',1,1,1,'0','nkz084732','kz084732','10086-10000-4008823823','234','2015-06-30','','','c#310','',0,'2015-05-31',1,'2015-06-01',0,'2015-06-01','',NULL,NULL,0,NULL,NULL,'',1,'',''),(4,1,'',1,3,1,'','ntx029412','tx029412','','','0000-00-00','','','','',0,'2015-05-31',0,'2015-06-01',0,'2015-06-01','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0,'',''),(6,1,'',1,2,1,'','nkx098472','kx098472','','','0000-00-00','','','','',0,'2015-05-31',0,'2015-06-01',0,'2015-06-01','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0,'',''),(7,1,'',1,3,1,'','ntx330032','tx330032','','','0000-00-00','','','','',0,'2015-05-31',0,'2015-06-01',0,'2015-06-01','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0,'',''),(8,1,'',1,2,1,'','ntt333333','tt333333','','','0000-00-00','','','','',0,'2015-05-31',0,'2015-06-01',0,'2015-06-01','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0,'',''),(9,1,'',1,4,1,'','ntx222222','tx222222','','','0000-00-00','','','','',0,'2015-05-31',0,'2015-06-01',0,'2015-06-01','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0,'',''),(10,1,'123',3,1,2,'0','nke222222','ke222222','123','123','2015-07-07','','','123','',0,'2015-05-31',1,'2015-06-01',0,'2015-06-01','',NULL,NULL,0,NULL,NULL,'',1,'',''),(11,3,'123',3,2,3,'0','nhe428421','he428421','123','123','2015-06-30','','','123','',0,'2015-05-31',1,'2015-06-01',0,'2015-06-01','',NULL,NULL,0,NULL,NULL,'',1,'',''),(12,1,'123',1,1,1,'0','213','123','123','123','2015-05-25','','','123','',0,'2015-05-31',0,'2015-05-31',0,'2015-05-31','0','2015-05-31','2015-05-31',1,'2015-05-31','2015-05-31','',1,'',''),(13,1,'123',1,1,1,'0','123','123','123','123','2015-06-22','','','123','',0,'2015-06-01',1,'2015-06-02',0,'2015-06-01','0','2015-06-01','2015-06-01',1,'2015-06-01','2015-06-01','',4,'','');

/*Table structure for table `devicemgt_k_device_spare` */

DROP TABLE IF EXISTS `devicemgt_k_device_spare`;

CREATE TABLE `devicemgt_k_device_spare` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k_device_id` int(11) NOT NULL,
  `k_spare_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `k_device_id` (`k_device_id`,`k_spare_id`),
  KEY `devicemgt_k_device_spare_b2f4ec6f` (`k_device_id`),
  KEY `devicemgt_k_device_spare_ec82079c` (`k_spare_id`),
  CONSTRAINT `k_device_id_refs_id_b9927edc` FOREIGN KEY (`k_device_id`) REFERENCES `devicemgt_k_device` (`id`),
  CONSTRAINT `k_spare_id_refs_id_9043de86` FOREIGN KEY (`k_spare_id`) REFERENCES `devicemgt_k_spare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_device_spare` */

/*Table structure for table `devicemgt_k_deviceplan` */

DROP TABLE IF EXISTS `devicemgt_k_deviceplan`;

CREATE TABLE `devicemgt_k_deviceplan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid_id` int(11) NOT NULL,
  `maintenanceid_id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `period` varchar(15) NOT NULL,
  `createcontent` varchar(100) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `assignorid` int(10) unsigned NOT NULL,
  `assigndatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_deviceplan_72537f95` (`deviceid_id`),
  KEY `devicemgt_k_deviceplan_221733ad` (`maintenanceid_id`),
  CONSTRAINT `deviceid_id_refs_id_e0de95d1` FOREIGN KEY (`deviceid_id`) REFERENCES `devicemgt_k_device` (`id`),
  CONSTRAINT `maintenanceid_id_refs_id_7574d147` FOREIGN KEY (`maintenanceid_id`) REFERENCES `devicemgt_k_maintenance` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_deviceplan` */

insert  into `devicemgt_k_deviceplan`(`id`,`deviceid_id`,`maintenanceid_id`,`title`,`period`,`createcontent`,`memo`,`assignorid`,`assigndatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,43,'556','halfmonth','778','990',1,'2015-06-05',9,'2015-06-05',0,'2015-06-05','0'),(2,1,44,'rrr','fourmonth','ttt','yyyy',1,'2015-06-05',8,'2015-06-05',0,'2015-06-05','0');

/*Table structure for table `devicemgt_k_devicetype` */

DROP TABLE IF EXISTS `devicemgt_k_devicetype`;

CREATE TABLE `devicemgt_k_devicetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentid` int(10) unsigned NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `name` varchar(30) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_devicetype` */

insert  into `devicemgt_k_devicetype`(`id`,`parentid`,`depth`,`name`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,0,0,'kernel','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(2,1,1,'sub_kernel1','',1,'2015-05-25',1,'2015-05-25',0,'2015-05-25','0'),(3,1,1,'sub_kernel2','',1,'2015-05-25',1,'2015-05-25',0,'2015-05-25','0'),(4,0,0,'kernel2','',1,'2015-05-25',1,'2015-05-25',0,'2015-05-25','0'),(5,2,2,'ssub_kernel1','',1,'2015-05-25',1,'2015-05-25',0,'2015-05-25','0'),(6,1,1,'哈哈哈','123',1,'2015-07-21',1,'2015-07-21',0,'2015-07-21','0'),(7,1,1,'冷水机组','',1,'2015-08-08',1,'2015-08-08',0,'2015-08-08','0'),(8,1,1,'冷却水泵','',1,'2015-08-08',1,'2015-08-08',0,'2015-08-08','0'),(9,1,1,'冷冻泵','',1,'2015-08-08',1,'2015-08-08',0,'2015-08-08','0');

/*Table structure for table `devicemgt_k_feedback` */

DROP TABLE IF EXISTS `devicemgt_k_feedback`;

CREATE TABLE `devicemgt_k_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(200) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_feedback` */

/*Table structure for table `devicemgt_k_form` */

DROP TABLE IF EXISTS `devicemgt_k_form`;

CREATE TABLE `devicemgt_k_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_form_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_5ea6c07b` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_form` */

insert  into `devicemgt_k_form`(`id`,`classid_id`,`content`,`brief`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'{data: 1}','kz084732',1,'2015-04-01',1,'2015-04-01',1,'2015-04-01','3'),(2,1,'{\"冷供水温度  ℃\": {\"type\": \"integer\",\"id\": \"0\",\"default\": \"\",\"priority\": \"0\",\"hint\":\"7-12\"}}','tx029412',1,'2015-04-02',1,'2015-04-02',1,'2015-04-02','3'),(3,1,'{data: 3}','kx098472',1,'2015-04-03',1,'2015-04-03',1,'2015-04-03','3'),(4,1,'{data: 4}','tx330032',1,'2015-04-04',1,'2015-04-04',1,'2015-04-04','3'),(5,1,'{\"水位\": {\"type\": \"integer\",\"id\": \"4\",\"default\": \"0\",\"priority\": \"4\",\"options\": {\"0\": \"偏高\",\"1\": \"中等\",\"2\": \"偏低\"}}}','tt333333',1,'2015-04-05',1,'2015-04-05',1,'2015-04-05','3'),(6,1,'{\"meta\": {\"type\": \"meta\",\"name\": \"Music Album\"},\"冷供水压力  Mpa\": {\"type\": \"integer\",\"id\": \"1\",\"default\": \"\",\"priority\": \"1\"}}','tx222222',1,'2015-04-06',1,'2015-04-06',1,'2015-04-06','3'),(7,1,'{\"冷供水温度  ℃\": {\"type\": \"integer\",\"id\": \"0\",\"default\": \"\",\"priority\": \"0\",\"hint\":\"7-12\"}}','ke222222',1,'2015-04-07',1,'2015-04-07',1,'2015-04-07','3'),(8,1,'{data: 8}','he428421',1,'2015-04-08',1,'2015-04-08',1,'2015-04-08','3'),(9,1,'','wd052813',0,'2015-06-05',0,'2015-06-05',0,'2015-06-05','0');

/*Table structure for table `devicemgt_k_formitem` */

DROP TABLE IF EXISTS `devicemgt_k_formitem`;

CREATE TABLE `devicemgt_k_formitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `formid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `datatype` varchar(1) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `lowerthreshold` varchar(30) NOT NULL,
  `upperthreshold` varchar(30) NOT NULL,
  `choices` varchar(100) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_formitem_432947aa` (`classid_id`),
  KEY `devicemgt_k_formitem_a6f496e6` (`formid_id`),
  CONSTRAINT `classid_id_refs_id_35b3b5fc` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `formid_id_refs_id_a81e9254` FOREIGN KEY (`formid_id`) REFERENCES `devicemgt_k_form` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_formitem` */

insert  into `devicemgt_k_formitem`(`id`,`classid_id`,`formid_id`,`name`,`datatype`,`unit`,`lowerthreshold`,`upperthreshold`,`choices`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (2,1,2,'machine status','1','-','-','-','normal/abnormal','very important',1,'2015-04-27',1,'2015-06-05',1,'2015-04-27','3'),(3,1,6,'','0','','','','-','',1,'2015-06-05',0,'2015-06-05',0,'2015-06-05','0'),(4,1,2,'pressure','0','MPa','12','18','-','important',1,'2015-06-05',0,'2015-06-05',0,'2015-06-05','0'),(5,1,4,'haha','0','123','1.3e10','','-','',1,'2015-06-05',1,'2015-06-05',0,'2015-06-05','0'),(6,1,5,'123','0','123','2432','2432','-','',1,'2015-06-05',1,'2015-06-05',0,'2015-06-05','0');

/*Table structure for table `devicemgt_k_maintenance` */

DROP TABLE IF EXISTS `devicemgt_k_maintenance`;

CREATE TABLE `devicemgt_k_maintenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `createcontent` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `editcontent` varchar(100) NOT NULL,
  `factor` int(10) unsigned NOT NULL,
  `memo` varchar(100) NOT NULL,
  `mtype` varchar(1) NOT NULL,
  `priority` varchar(1) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `assignorid` int(10) unsigned NOT NULL,
  `assigndatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_maintenance_72537f95` (`deviceid_id`),
  CONSTRAINT `deviceid_id_refs_id_e790c6dd` FOREIGN KEY (`deviceid_id`) REFERENCES `devicemgt_k_device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_maintenance` */

insert  into `devicemgt_k_maintenance`(`id`,`deviceid_id`,`state`,`title`,`createcontent`,`image`,`editcontent`,`factor`,`memo`,`mtype`,`priority`,`creatorid`,`createdatetime`,`assignorid`,`assigndatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (26,2,'3','m2','too old','','',1,'','2','1',1,'2015-04-29',2,'2015-04-29',4,'2015-04-29',0,'2015-04-29','0'),(30,2,'3','m6','leaking','','ok!',3,'345','2','2',1,'2015-05-01',2,'2015-05-01',3,'2015-05-01',0,'2015-05-08','0'),(31,2,'3','m7','parts loosening','','不行么？',2,'456','2','3',1,'2015-05-01',2,'2015-05-01',4,'2015-05-01',0,'2015-05-01','0'),(36,2,'3','k3','c3','','ok',3,'x','2','',1,'2015-05-05',2,'2015-04-30',5,'2015-05-01',0,'2015-05-05','0'),(37,2,'3','k4','c4','','测试',2,'x','1','',1,'2015-05-05',2,'2015-04-30',6,'2015-05-01',0,'2015-05-05','0'),(40,2,'4','k7','c7','','ok',1,'x','1','',1,'2015-05-05',2,'2015-05-01',5,'2015-05-05',0,'2015-05-05','0'),(42,1,'2','shuigunhuaile','c#301','','',1,'..','2','2',1,'2015-05-08',2,'2015-05-08',5,'2015-05-08',0,'2015-05-08','0'),(43,1,'2','556','778','','开始',1,'990','1','1',1,'2015-06-05',2,'2015-06-05',9,'2015-06-05',0,'2015-06-05','0'),(44,1,'2','rrr','ttt','','',1,'yyyy','1','1',1,'2015-06-05',2,'2015-06-05',8,'2015-06-05',0,'2015-06-05','0');

/*Table structure for table `devicemgt_k_meter` */

DROP TABLE IF EXISTS `devicemgt_k_meter`;

CREATE TABLE `devicemgt_k_meter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brief` varchar(50) NOT NULL,
  `routeid_id` int(11) DEFAULT NULL,
  `userid_id` int(11) DEFAULT NULL,
  `metertime` datetime NOT NULL,
  `json` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_meter_8154c9fe` (`routeid_id`),
  KEY `devicemgt_k_meter_936913d1` (`userid_id`),
  CONSTRAINT `routeid_id_refs_id_030bd83d` FOREIGN KEY (`routeid_id`) REFERENCES `devicemgt_k_route` (`id`),
  CONSTRAINT `userid_id_refs_id_76082153` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_meter` */

/*Table structure for table `devicemgt_k_producer` */

DROP TABLE IF EXISTS `devicemgt_k_producer`;

CREATE TABLE `devicemgt_k_producer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `contact` varchar(30) NOT NULL,
  `addr` varchar(80) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `linkman` varchar(30) NOT NULL,
  `mobile` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_producer` */

insert  into `devicemgt_k_producer`(`id`,`name`,`contact`,`addr`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`linkman`,`mobile`) values (1,'TSINGH','18810305382','DHHH','s',0,'2015-05-04',1,'2015-05-22','',''),(2,'PKEING','18060198885','HDDD1','11111',0,'2015-05-22',1,'2015-05-22','',''),(3,'test1','test','test','112',0,'2015-05-22',1,'2015-05-22','',''),(4,'changjia1','email','188','',1,'2015-05-25',1,'2015-05-25','hahaha','100'),(5,'格兰富','1','1','',1,'2015-08-08',1,'2015-08-08','1','1'),(6,'特灵','1','1','',1,'2015-08-08',1,'2015-08-08','1','1'),(7,'良机','1','1','',1,'2015-08-08',1,'2015-08-08','1','1');

/*Table structure for table `devicemgt_k_project` */

DROP TABLE IF EXISTS `devicemgt_k_project`;

CREATE TABLE `devicemgt_k_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `meterscore` int(10) unsigned NOT NULL,
  `maintenancescore` int(10) unsigned NOT NULL,
  `taskscore` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_project_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_d573ce4b` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_project` */

/*Table structure for table `devicemgt_k_purview` */

DROP TABLE IF EXISTS `devicemgt_k_purview`;

CREATE TABLE `devicemgt_k_purview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `item` varchar(20) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_purview_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_92b6dd49` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_purview` */

insert  into `devicemgt_k_purview`(`id`,`classid_id`,`name`,`item`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'分类','查看','您没有查看分类的权限',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(2,1,'分类','添加/编辑','您没有添加/编辑分类的权限',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(3,1,'分类','审核/删除','您没有审核/删除分类的权限',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(4,1,'角色','查看','您没有查看角色的权限',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(5,1,'角色','添加/编辑','您没有添加/编辑角色的权限',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(6,1,'角色','审核/删除','您没有审核/删除角色的权限',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(7,1,'用户','查看','您没有查看用户的权限',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(8,1,'用户','添加/编辑','您没有添加/编辑用户的权限',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(9,1,'用户','审核/删除','您没有审核/删除用户的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(10,1,'设备分类','查看','您没有查看设备分类的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(11,1,'设备分类','添加/编辑','您没有添加/编辑设备分类的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(12,1,'设备分类','审核/删除','您没有审核/删除设备分类的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(13,1,'设备厂商','查看','您没有查看设备厂商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(14,1,'设备厂商','添加/编辑','您没有添加/编辑设备厂商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(15,1,'设备厂商','审核/删除','您没有审核/删除设备厂商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(16,1,'供应商','查看','您没有查看供应商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(17,1,'供应商','添加/编辑','您没有添加/编辑供应商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(18,1,'供应商','审核/删除','您没有审核/删除供应商的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(19,1,'设备','查看','您没有查看设备的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(20,1,'设备','添加/编辑','您没有添加/编辑设备的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(21,1,'设备','审核/删除','您没有审核/删除设备的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(22,1,'备件信息','查看','您没有查看备件信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(23,1,'备件信息','添加/编辑','您没有添加/编辑备件信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(24,1,'备件信息','审核/删除','您没有审核/删除备件信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(25,1,'工具信息','查看','您没有查看工具信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(26,1,'工具信息','添加/编辑','您没有添加/编辑工具信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(27,1,'工具信息','审核/删除','您没有审核/删除工具信息的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(28,1,'保养','查看','您没有查看保养的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(29,1,'保养','添加/编辑','您没有添加/编辑保养的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(30,1,'保养','审核/删除','您没有审核/删除保养的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(31,1,'维修','查看','您没有查看维修的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(32,1,'维修','指派','您没有指派维修的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(33,1,'维修','添加/编辑','您没有添加/编辑维修的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(34,1,'维修','审核/删除','您没有审核/删除维修的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(35,1,'任务','查看','您没有查看任务的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(37,1,'任务','添加/编辑','您没有添加/编辑任务的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(38,1,'任务','审核/删除','您没有审核/删除任务的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(39,1,'备件库存','查看','您没有查看备件库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(40,1,'备件库存','添加/编辑','您没有添加/编辑备件库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(41,1,'备件库存','审核/删除','您没有审核/删除备件库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(42,1,'工具库存','查看','您没有查看工具库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(43,1,'工具库存','添加/编辑','您没有添加/编辑工具库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(44,1,'工具库存','审核/删除','您没有审核/删除工具库存的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00',''),(45,1,'抄表','查看','您没有查看抄表的权限',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00','');

/*Table structure for table `devicemgt_k_role` */

DROP TABLE IF EXISTS `devicemgt_k_role`;

CREATE TABLE `devicemgt_k_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_role_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_fdd4c13d` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_role` */

insert  into `devicemgt_k_role`(`id`,`classid_id`,`name`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'purview_design','312',1,'2015-04-07',1,'2015-04-21',1,'2015-04-15','3'),(2,1,'information_audition','31232',1,'2015-04-15',1,'2015-04-15',1,'2015-04-17','3'),(6,1,'123','',1,'2015-06-05',1,'2015-06-23',0,'2015-06-05','0'),(7,6,'12345','',1,'2015-06-05',1,'2015-06-05',0,'2015-06-05','0'),(8,5,'ffff','',1,'2015-06-05',1,'2015-06-05',0,'2015-06-05','0'),(9,1,'所有查看','',1,'2015-06-26',1,'2015-06-26',0,'2015-06-26','0'),(10,1,'所有添加/编辑','',1,'2015-06-26',1,'2015-06-26',0,'2015-06-26','0'),(11,1,'所有审核/删除','',1,'2015-06-26',1,'2015-06-26',0,'2015-06-26','0'),(12,1,'所有权限','',1,'2015-06-26',1,'2015-06-26',0,'2015-06-26','0');

/*Table structure for table `devicemgt_k_role_purviews` */

DROP TABLE IF EXISTS `devicemgt_k_role_purviews`;

CREATE TABLE `devicemgt_k_role_purviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k_role_id` int(11) NOT NULL,
  `k_purview_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `k_role_id` (`k_role_id`,`k_purview_id`),
  KEY `devicemgt_k_role_purviews_893707b2` (`k_role_id`),
  KEY `devicemgt_k_role_purviews_7b0e22a5` (`k_purview_id`),
  CONSTRAINT `k_purview_id_refs_id_f7485864` FOREIGN KEY (`k_purview_id`) REFERENCES `devicemgt_k_purview` (`id`),
  CONSTRAINT `k_role_id_refs_id_21374a3f` FOREIGN KEY (`k_role_id`) REFERENCES `devicemgt_k_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_role_purviews` */

insert  into `devicemgt_k_role_purviews`(`id`,`k_role_id`,`k_purview_id`) values (12,1,1),(11,1,2),(10,1,3),(6,2,1),(9,2,2),(7,2,3),(36,6,34),(17,7,1),(32,8,1),(33,8,2),(35,8,3),(48,9,1),(49,9,4),(50,9,7),(37,9,10),(38,9,13),(40,9,16),(41,9,19),(39,9,22),(51,9,25),(42,9,28),(43,9,31),(47,9,35),(46,9,39),(45,9,42),(44,9,45),(63,10,2),(64,10,5),(65,10,8),(52,10,11),(55,10,14),(56,10,17),(54,10,20),(57,10,23),(53,10,26),(60,10,29),(58,10,33),(59,10,37),(61,10,40),(62,10,43),(75,11,3),(77,11,6),(78,11,9),(67,11,12),(68,11,15),(70,11,18),(69,11,21),(66,11,24),(74,11,27),(72,11,30),(73,11,34),(76,11,38),(79,11,41),(71,11,44),(96,12,1),(98,12,2),(97,12,3),(100,12,4),(99,12,5),(102,12,6),(101,12,7),(104,12,8),(103,12,9),(108,12,10),(107,12,11),(106,12,12),(105,12,13),(112,12,14),(111,12,15),(114,12,16),(113,12,17),(116,12,18),(115,12,19),(86,12,20),(87,12,21),(88,12,22),(89,12,23),(82,12,24),(83,12,25),(84,12,26),(85,12,27),(92,12,28),(81,12,29),(118,12,30),(117,12,31),(124,12,32),(123,12,33),(122,12,34),(121,12,35),(119,12,37),(110,12,38),(109,12,39),(94,12,40),(95,12,41),(80,12,42),(93,12,43),(90,12,44),(91,12,45);

/*Table structure for table `devicemgt_k_route` */

DROP TABLE IF EXISTS `devicemgt_k_route`;

CREATE TABLE `devicemgt_k_route` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `formid` varchar(80) NOT NULL,
  `starttime` time NOT NULL,
  `period` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_route_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_baa2a870` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_route` */

insert  into `devicemgt_k_route`(`id`,`classid_id`,`name`,`formid`,`starttime`,`period`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'route1','2,5,6,7','08:00:00',2,1,'2015-04-01',1,'2015-04-23',1,'2015-04-01','3'),(2,1,'route2','1,5,8','10:00:00',3,1,'2015-04-01',1,'2015-04-01',1,'2015-04-01','3');

/*Table structure for table `devicemgt_k_schedule` */

DROP TABLE IF EXISTS `devicemgt_k_schedule`;

CREATE TABLE `devicemgt_k_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `route_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_schedule_432947aa` (`classid_id`),
  KEY `devicemgt_k_schedule_854631fb` (`route_id`),
  KEY `devicemgt_k_schedule_6340c63c` (`user_id`),
  CONSTRAINT `classid_id_refs_id_4dc8fa60` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `route_id_refs_id_bcf0225a` FOREIGN KEY (`route_id`) REFERENCES `devicemgt_k_route` (`id`),
  CONSTRAINT `user_id_refs_id_af05aa4f` FOREIGN KEY (`user_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_schedule` */

insert  into `devicemgt_k_schedule`(`id`,`classid_id`,`route_id`,`user_id`,`date`) values (1,1,1,2,'2015-07-21'),(2,1,2,2,'2015-06-27');

/*Table structure for table `devicemgt_k_spare` */

DROP TABLE IF EXISTS `devicemgt_k_spare`;

CREATE TABLE `devicemgt_k_spare` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `brand` varchar(30) NOT NULL,
  `producerid_id` int(11) NOT NULL,
  `model` varchar(30) NOT NULL,
  `supplierid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `minimum` int(10) unsigned NOT NULL,
  `eligiblestock` int(10) unsigned NOT NULL,
  `ineligiblestock` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_spare_432947aa` (`classid_id`),
  KEY `devicemgt_k_spare_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_spare_69308dea` (`supplierid_id`),
  CONSTRAINT `classid_id_refs_id_0b558ac8` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_9fd74a5a` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_b2e6caa3` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_spare` */

insert  into `devicemgt_k_spare`(`id`,`classid_id`,`name`,`brief`,`brand`,`producerid_id`,`model`,`supplierid_id`,`content`,`memo`,`minimum`,`eligiblestock`,`ineligiblestock`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (11,7,'spare1','s1_1','b1',1,'mo1',1,'c1','me1',20,30,0,1,'2015-05-24',1,'2015-06-05',0,'2015-05-24','0'),(12,6,'s12','s11','b1',3,'m1',3,'c1','',3,0,0,1,'2015-06-05',1,'2015-06-05',0,'2015-06-05','0'),(13,1,'是','是','是',1,'是',1,'是','',12,0,0,1,'2015-07-21',0,'2015-07-21',0,'2015-07-21','0');

/*Table structure for table `devicemgt_k_sparebill` */

DROP TABLE IF EXISTS `devicemgt_k_sparebill`;

CREATE TABLE `devicemgt_k_sparebill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `spareid_id` int(11) NOT NULL,
  `using` int(10) unsigned NOT NULL,
  `returned` int(10) unsigned NOT NULL,
  `depleted` int(10) unsigned NOT NULL,
  `damaged` int(10) unsigned NOT NULL,
  `rejected` int(10) unsigned NOT NULL,
  `user` varchar(10) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_sparebill_432947aa` (`classid_id`),
  KEY `devicemgt_k_sparebill_12fc9209` (`spareid_id`),
  CONSTRAINT `classid_id_refs_id_4ffbefc7` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `spareid_id_refs_id_8eee649a` FOREIGN KEY (`spareid_id`) REFERENCES `devicemgt_k_spare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_sparebill` */

/*Table structure for table `devicemgt_k_sparecount` */

DROP TABLE IF EXISTS `devicemgt_k_sparecount`;

CREATE TABLE `devicemgt_k_sparecount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `sparebillid` int(10) unsigned NOT NULL,
  `spareid_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `iseligible` varchar(1) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_sparecount_432947aa` (`classid_id`),
  KEY `devicemgt_k_sparecount_12fc9209` (`spareid_id`),
  CONSTRAINT `classid_id_refs_id_9a8f3ea4` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `spareid_id_refs_id_c63e4168` FOREIGN KEY (`spareid_id`) REFERENCES `devicemgt_k_spare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_sparecount` */

/*Table structure for table `devicemgt_k_sparecount_maintenanceid` */

DROP TABLE IF EXISTS `devicemgt_k_sparecount_maintenanceid`;

CREATE TABLE `devicemgt_k_sparecount_maintenanceid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k_sparecount_id` int(11) NOT NULL,
  `k_maintenance_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `k_sparecount_id` (`k_sparecount_id`,`k_maintenance_id`),
  KEY `devicemgt_k_sparecount_maintenanceid_7f95069c` (`k_sparecount_id`),
  KEY `devicemgt_k_sparecount_maintenanceid_a0433d4b` (`k_maintenance_id`),
  CONSTRAINT `k_maintenance_id_refs_id_d186555a` FOREIGN KEY (`k_maintenance_id`) REFERENCES `devicemgt_k_maintenance` (`id`),
  CONSTRAINT `k_sparecount_id_refs_id_ed63e7e8` FOREIGN KEY (`k_sparecount_id`) REFERENCES `devicemgt_k_sparecount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_sparecount_maintenanceid` */

/*Table structure for table `devicemgt_k_staffegginfo` */

DROP TABLE IF EXISTS `devicemgt_k_staffegginfo`;

CREATE TABLE `devicemgt_k_staffegginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid_id` int(11) NOT NULL,
  `time` date NOT NULL,
  `bonus` double NOT NULL,
  `probability` double NOT NULL,
  `state` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_staffegginfo_936913d1` (`userid_id`),
  CONSTRAINT `userid_id_refs_id_95587539` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_staffegginfo` */

insert  into `devicemgt_k_staffegginfo`(`id`,`userid_id`,`time`,`bonus`,`probability`,`state`) values (1,2,'2015-07-19',20,0.05,'0'),(2,2,'2015-07-20',20,0.1,'0'),(3,10,'2015-07-20',20,0.1,'0');

/*Table structure for table `devicemgt_k_staffscoreinfo` */

DROP TABLE IF EXISTS `devicemgt_k_staffscoreinfo`;

CREATE TABLE `devicemgt_k_staffscoreinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid_id` int(11) NOT NULL,
  `score` int(10) unsigned NOT NULL,
  `content` varchar(80) NOT NULL,
  `time` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_staffscoreinfo_936913d1` (`userid_id`),
  CONSTRAINT `userid_id_refs_id_760427ab` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_staffscoreinfo` */

insert  into `devicemgt_k_staffscoreinfo`(`id`,`userid_id`,`score`,`content`,`time`) values (1,1,34,'test','2015-07-01'),(2,2,12,'test','2015-07-24');

/*Table structure for table `devicemgt_k_staffworkinfo` */

DROP TABLE IF EXISTS `devicemgt_k_staffworkinfo`;

CREATE TABLE `devicemgt_k_staffworkinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `checkin` varchar(80) NOT NULL,
  `checkout` varchar(80) NOT NULL,
  `shifting` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_staffworkinfo_936913d1` (`userid_id`),
  CONSTRAINT `userid_id_refs_id_9174919c` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_staffworkinfo` */

/*Table structure for table `devicemgt_k_supplier` */

DROP TABLE IF EXISTS `devicemgt_k_supplier`;

CREATE TABLE `devicemgt_k_supplier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `contact` varchar(30) NOT NULL,
  `addr` varchar(80) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `linkman` varchar(30) NOT NULL,
  `mobile` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_supplier` */

insert  into `devicemgt_k_supplier`(`id`,`name`,`contact`,`addr`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`linkman`,`mobile`) values (1,'RENMING','15459541233','HUAQING','notice',0,'2015-05-12',0,'0000-00-00','',''),(2,'JIAOTONG','13950801816','HAIDIAN','HIGH',1,'2015-05-22',1,'2015-05-22','',''),(3,'test2','12','222','',1,'2015-05-22',1,'2015-05-22','',''),(4,'12323','12','1222','11',1,'2015-05-22',1,'2015-05-22','',''),(5,'特灵','1','1','',1,'2015-08-08',1,'2015-08-08','1','1');

/*Table structure for table `devicemgt_k_task` */

DROP TABLE IF EXISTS `devicemgt_k_task`;

CREATE TABLE `devicemgt_k_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `createcontent` varchar(100) NOT NULL,
  `editcontent` varchar(100) NOT NULL,
  `auditcontent` varchar(100) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `priority` varchar(1) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_task` */

insert  into `devicemgt_k_task`(`id`,`state`,`title`,`createcontent`,`editcontent`,`auditcontent`,`memo`,`priority`,`creatorid`,`createdatetime`,`auditorid`,`auditdatetime`,`status`) values (6,'1','123','333','','','333','1',1,'2015-05-05',0,'2015-05-05','0'),(7,'1','456','777','','','32','2',1,'2015-05-05',0,'2015-05-05','0'),(8,'2','111','22','','','3','3',1,'2015-05-05',0,'2015-05-05','0'),(9,'1','ew','ewew','','','','2',1,'2015-05-05',0,'2015-05-05','0'),(10,'3','gg','hh','','','jj','1',1,'2015-05-05',0,'2015-05-05','0'),(11,'4','ff','fff','','','ffff','1',1,'2015-05-05',0,'2015-05-05','0');

/*Table structure for table `devicemgt_k_taskitem` */

DROP TABLE IF EXISTS `devicemgt_k_taskitem`;

CREATE TABLE `devicemgt_k_taskitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `taskid_id` int(11) NOT NULL,
  `createcontent` varchar(100) NOT NULL,
  `editcontent` varchar(100) NOT NULL,
  `auditcontent` varchar(100) NOT NULL,
  `factor` int(10) unsigned NOT NULL,
  `memo` varchar(100) NOT NULL,
  `priority` varchar(1) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_taskitem_752fe31f` (`taskid_id`),
  CONSTRAINT `taskid_id_refs_id_1ab584ad` FOREIGN KEY (`taskid_id`) REFERENCES `devicemgt_k_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_taskitem` */

insert  into `devicemgt_k_taskitem`(`id`,`state`,`title`,`taskid_id`,`createcontent`,`editcontent`,`auditcontent`,`factor`,`memo`,`priority`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (5,'2','sub3',6,'xilian','','',0,'354','3',1,'2015-05-12',6,'2015-05-12',0,'2015-05-12','1'),(6,'3','sub4',6,'zaofan','chiwanle','',2,'0','2',1,'2015-05-12',3,'2015-05-12',1,'2015-05-12','1'),(7,'4','sub5',6,'shangban','shangwanle','',2,'9','2',1,'2015-05-12',6,'2015-05-12',1,'2015-05-13','1'),(12,'1','sub6',6,'xiaban','','',1,'haha','3',1,'2015-05-13',4,'2015-05-13',0,'2015-05-13','0'),(13,'1','re',9,'ewr','','',1,'rew','2',1,'2015-05-13',9,'2015-05-13',0,'2015-05-13','0');

/*Table structure for table `devicemgt_k_tool` */

DROP TABLE IF EXISTS `devicemgt_k_tool`;

CREATE TABLE `devicemgt_k_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `brief` varchar(50) NOT NULL,
  `brand` varchar(50) NOT NULL,
  `producerid_id` int(11) NOT NULL,
  `model` varchar(50) NOT NULL,
  `supplierid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `minimum` int(10) unsigned NOT NULL,
  `eligiblestock` int(10) unsigned NOT NULL,
  `ineligiblestock` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  `ownerid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_tool_432947aa` (`classid_id`),
  KEY `devicemgt_k_tool_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_tool_69308dea` (`supplierid_id`),
  KEY `devicemgt_k_tool_c128a093` (`ownerid_id`),
  CONSTRAINT `classid_id_refs_id_67fdcf25` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `ownerid_id_refs_id_67fdcf25` FOREIGN KEY (`ownerid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_1d6747ec` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_ea0efb3f` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_tool` */

insert  into `devicemgt_k_tool`(`id`,`classid_id`,`name`,`brief`,`brand`,`producerid_id`,`model`,`supplierid_id`,`content`,`memo`,`minimum`,`eligiblestock`,`ineligiblestock`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`,`ownerid_id`) values (1,1,'tool1','t1','b1',1,'m1',1,'123','',30,0,0,1,'2015-07-21',1,'2015-07-21',0,'2015-07-21','0',3);

/*Table structure for table `devicemgt_k_toolcount` */

DROP TABLE IF EXISTS `devicemgt_k_toolcount`;

CREATE TABLE `devicemgt_k_toolcount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `tooluseid` int(10) unsigned NOT NULL,
  `toolid_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `iseligible` varchar(1) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_toolcount_432947aa` (`classid_id`),
  KEY `devicemgt_k_toolcount_9e808b4a` (`toolid_id`),
  CONSTRAINT `classid_id_refs_id_639b3160` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `toolid_id_refs_id_bf3b36c6` FOREIGN KEY (`toolid_id`) REFERENCES `devicemgt_k_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_toolcount` */

/*Table structure for table `devicemgt_k_tooluse` */

DROP TABLE IF EXISTS `devicemgt_k_tooluse`;

CREATE TABLE `devicemgt_k_tooluse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `toolid_id` int(11) NOT NULL,
  `using` int(10) unsigned NOT NULL,
  `returned` int(10) unsigned NOT NULL,
  `depleted` int(10) unsigned NOT NULL,
  `damaged` int(10) unsigned NOT NULL,
  `rejected` int(10) unsigned NOT NULL,
  `user` varchar(10) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_tooluse_432947aa` (`classid_id`),
  KEY `devicemgt_k_tooluse_9e808b4a` (`toolid_id`),
  CONSTRAINT `classid_id_refs_id_b7701519` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `toolid_id_refs_id_28000472` FOREIGN KEY (`toolid_id`) REFERENCES `devicemgt_k_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_tooluse` */

/*Table structure for table `devicemgt_k_user` */

DROP TABLE IF EXISTS `devicemgt_k_user`;

CREATE TABLE `devicemgt_k_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(128) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `face` varchar(30) NOT NULL,
  `mobile` varchar(50) NOT NULL,
  `email` varchar(75) NOT NULL,
  `address` varchar(80) NOT NULL,
  `zipcode` varchar(30) NOT NULL,
  `birthday` date NOT NULL,
  `idcard` varchar(30) NOT NULL,
  `idcardtype` varchar(1) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `contact` varchar(30) NOT NULL,
  `contactmobile` varchar(30) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  `todo` int(10) unsigned NOT NULL,
  `onlinetime` int(10) unsigned NOT NULL,
  `avatar` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_user_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_6b588af6` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_user` */

insert  into `devicemgt_k_user`(`id`,`classid_id`,`state`,`username`,`password`,`name`,`gender`,`face`,`mobile`,`email`,`address`,`zipcode`,`birthday`,`idcard`,`idcardtype`,`content`,`memo`,`contact`,`contactmobile`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`,`todo`,`onlinetime`,`avatar`) values (1,1,'','hahehi','pbkdf2_sha256$12000$fbLvT2mV7bcZ$UgljjZePlWiXO83O5fBCY/iLDAp+BBhClOSiAyEOMyw=','zhangsan','1','../static/images/user.png','15959540000','hahehi@qq.com','406B','100084','1992-09-01','','','','','','',0,'2015-04-29',1,'2015-07-21',0,'2015-04-29','',0,0,''),(2,2,'','syb1001','pbkdf2_sha256$15000$K9T73jen4wHH$LyqQHJblrPwXsak+/Hnl18vjSdBPkoTYKFGb3jKT+bE=','lisi','1','../static/images/user.png','132********','syb@qq.com','','','2015-04-29','','','','','','',0,'2015-04-29',0,'2015-04-29',0,'2015-04-29','',0,0,''),(3,3,'','yl-1993','yl','wangwu','1','../static/images/user.png','yl188','yl@qq.com','','','2015-04-29','','','','','','',0,'2015-04-29',0,'2015-04-29',0,'2015-04-29','',0,0,''),(4,3,'','wenqf11','wqf','chenliu','1','../static/images/user.png','wqf188','wqf@qq.com','','','2015-04-29','','','','','','',0,'2015-04-29',0,'2015-04-29',0,'2015-04-29','',0,0,''),(5,5,'1','test1','123','','1','../static/images/user.png','','','','','1993-05-28','','0','','','','',0,'2015-05-01',1,'2015-05-23',0,'2015-05-01','0',0,0,''),(6,5,'1','user1','pbkdf2_sha256$10000$ykDJrrNndgrZ$l0SFaaQhZP8VDTd6CJGljWkIYKQtcyRersT/xopxKhM=','user1','1','../static/images/user.png','18810305385','691@qq.com','','','1993-05-28','','0','','','','',0,'2015-05-01',0,'2015-05-01',0,'2015-05-01','0',0,0,''),(7,2,'1','user2','pbkdf2_sha256$10000$PSfY4NA9p7Ga$ZYJGpjWR2m05ynL4+DSVTIoh1wIH/KsDOm9PlYAu7Hg=','user2','1','../static/images/user.png','18810305383','691w@qq.com','','','1993-05-28','','0','','','','',0,'2015-05-01',0,'2015-05-01',0,'2015-05-01','0',0,0,''),(8,7,'1','user3','pbkdf2_sha256$10000$DmZNtTUwnxw4$8ubToZomThUK9wBk/mGiIyVChRpXHcLUMKCItDAya5Y=','user3','1','../static/images/user.png','18810305382','69@qq.com','','','1993-05-28','','0','','','','',0,'2015-05-01',0,'2015-05-01',0,'2015-05-01','0',0,0,''),(9,8,'1','user4','pbkdf2_sha256$10000$pH2ghR1OiXOo$tvom0zCO9G6rZnDVqt50xAPgHNvJpQdzkBcKbJfqDeQ=','user4','1','../static/images/user.png','18810305381','6987@qq.com','','','1993-05-28','','0','','','','',0,'2015-05-01',0,'2015-05-01',0,'2015-05-01','0',0,0,''),(10,2,'1','wenqingfu','pbkdf2_sha256$12000$NvuVjfuvXiSx$wURHFD4oqXuI3WSaXyTxTkcuFjpuTl9M0IncCEQ3HuU=','文庆福','1','../static/images/user.png','13681332621','thssvince@163.com','','','1993-02-04','431224199302041099','0','','','李某某','13681332222',0,'2015-07-20',0,'2015-07-20',0,'2015-07-20','0',0,0,''),(11,1,'1','lxf','pbkdf2_sha256$10000$C8lc38XNE04Q$2IUxq1i1DezNdEfs7mAEOlF4vWtzBR+3lvDY47MQWYo=','lxf','1','../static/images/user.png','1','1','1','1','2015-08-08','1','0','','','1','18810305382',0,'2015-08-08',0,'2015-08-08',0,'2015-08-08','0',0,0,'user_avatar/undefined.png');

/*Table structure for table `devicemgt_k_user_roles` */

DROP TABLE IF EXISTS `devicemgt_k_user_roles`;

CREATE TABLE `devicemgt_k_user_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k_user_id` int(11) NOT NULL,
  `k_role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `k_user_id` (`k_user_id`,`k_role_id`),
  KEY `devicemgt_k_user_roles_0abdc8da` (`k_user_id`),
  KEY `devicemgt_k_user_roles_893707b2` (`k_role_id`),
  CONSTRAINT `k_role_id_refs_id_85e9cbb2` FOREIGN KEY (`k_role_id`) REFERENCES `devicemgt_k_role` (`id`),
  CONSTRAINT `k_user_id_refs_id_25e7ab78` FOREIGN KEY (`k_user_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

/*Data for the table `devicemgt_k_user_roles` */

insert  into `devicemgt_k_user_roles`(`id`,`k_user_id`,`k_role_id`) values (27,1,9),(28,1,12),(8,5,1),(2,6,1),(3,7,1),(6,8,1),(7,9,1),(26,10,1),(29,11,1);

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'k_class','devicemgt','k_class'),(9,'k_purview','devicemgt','k_purview'),(10,'k_role','devicemgt','k_role'),(11,'k_classrole','devicemgt','k_classrole'),(12,'k_user','devicemgt','k_user'),(13,'k_devicetype','devicemgt','k_devicetype'),(14,'k_supplier','devicemgt','k_supplier'),(15,'k_producer','devicemgt','k_producer'),(16,'k_spare','devicemgt','k_spare'),(17,'k_device','devicemgt','k_device'),(18,'k_form','devicemgt','k_form'),(19,'k_formitem','devicemgt','k_formitem'),(20,'k_route','devicemgt','k_route'),(21,'k_meter','devicemgt','k_meter'),(22,'k_maintenance','devicemgt','k_maintenance'),(23,'k_task','devicemgt','k_task'),(24,'k_taskitem','devicemgt','k_taskitem'),(25,'k_sparebill','devicemgt','k_sparebill'),(26,'k_sparecount','devicemgt','k_sparecount'),(27,'k_tool','devicemgt','k_tool'),(28,'k_tooluse','devicemgt','k_tooluse'),(29,'k_toolcount','devicemgt','k_toolcount'),(30,'k_project','devicemgt','k_project'),(31,'k_schedule','devicemgt','k_schedule'),(32,'k_staffworkinfo','devicemgt','k_staffworkinfo'),(33,'k_staffscoreinfo','devicemgt','k_staffscoreinfo'),(34,'k_staffegginfo','devicemgt','k_staffegginfo'),(35,'k_feedback','devicemgt','k_feedback'),(36,'k_deviceplan','devicemgt','k_deviceplan'),(37,'k_config','devicemgt','k_config');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values (1,'contenttypes','0001_initial','2015-04-12 13:17:18'),(2,'auth','0001_initial','2015-04-12 13:17:26'),(3,'admin','0001_initial','2015-04-12 13:17:30'),(4,'sessions','0001_initial','2015-04-12 13:17:30'),(5,'sites','0001_initial','2015-04-12 13:17:31');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values ('1hqtsj67xy2htrmme7lob3gqlrxzvw64','N2IyMmU0MDc1OTg3NWY3YmEzMmUzNTk0YzNjNzkzODA4Y2E4OWUwNTqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==','2015-08-14 06:18:09'),('3m1r0wtvvbctg0hkc77hvvpp3e99cl4a','NDIzYmFjOWNlY2NkNzRmYTViMTQ1ZjY1ZGE3OTIwNTg2YTU5Yjk1Mjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2015-07-07 13:38:24'),('8gj8uf37xj44aer1ucn5mzy38nekzmt0','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-08-04 11:16:12'),('8lhsh9oulqek6tpblczdm5occoug3mqf','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-05-14 07:58:02'),('bdsp4ls3yt2wlje64pyxw1e89db2fqld','N2IyMmU0MDc1OTg3NWY3YmEzMmUzNTk0YzNjNzkzODA4Y2E4OWUwNTqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==','2015-06-13 03:27:08'),('cvdapyh4653ibwt4lgdl3jay8o79lht4','N2IyMmU0MDc1OTg3NWY3YmEzMmUzNTk0YzNjNzkzODA4Y2E4OWUwNTqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==','2015-08-12 05:27:24'),('eioghmljg0d33i6hhay1rrnh93nuojpo','ODNjZjBkY2Q5ZTU4ZGEzOWZiMGVlZDZjYzI0ZmZiOGQ1NjlkMTY1MzqAAn1xAShVDV9hdXRoX3VzZXJfaWSKAQFVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxAnUu','2015-06-06 03:07:17'),('if0bcle58w0z5crrktpqypg8dtj2a8jz','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-05-26 12:00:49'),('j7ayg5ybca30nafokphrvxdfmkb0qr3h','ZWMzNTg1OTk1NDBjZWEzZTBjYjQ1MTE1ZGI2ZTc0MjAyZTY3ZTFlYjp7Il9hdXRoX3VzZXJfaGFzaCI6IjdjZTQyZWMzNjY5NWIyYTc4MzBjYjgxZjk2YWY3N2ZiNmZlMjdlZTgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9','2015-05-05 13:47:54'),('l4hjep2nt19rl1uw84p1t8syla3jjvan','NDIzYmFjOWNlY2NkNzRmYTViMTQ1ZjY1ZGE3OTIwNTg2YTU5Yjk1Mjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2015-08-03 12:18:15'),('le6stkwdheqyvtwi5uj5mi3or35lug6p','NjI1ZDIxMzk4ZmEyMjdkZTViZTBlMjJlMTVhMmM0Y2MzN2MzMzUxNDp7Il9hdXRoX3VzZXJfaGFzaCI6IjkxY2M3YTQ2NzI4ODEzOWM4MDM1N2FjNzdlYWU5YmQ1MzAxOWJmZmEiLCJfYXV0aF91c2VyX2lkIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2015-08-01 04:20:40'),('p3uo1lg5ave4shjekcmxhekwnto4a49g','N2IyMmU0MDc1OTg3NWY3YmEzMmUzNTk0YzNjNzkzODA4Y2E4OWUwNTqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==','2015-05-08 14:33:28'),('qnycv2lb6i7mymhaaemqbzaval2fl8h2','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-04-27 12:18:19'),('skw8slv7enk0sxdgzhacbp241p9amjbc','NDIzYmFjOWNlY2NkNzRmYTViMTQ1ZjY1ZGE3OTIwNTg2YTU5Yjk1Mjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2015-05-05 13:31:24'),('un4cbhq8i8zup2egzqtflzuuwhomxzy6','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-05-11 07:52:20'),('vgxpruqu8f7cbgiu3ythrn5h86lzl168','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-08-03 12:18:54'),('zxdvlyja9lkxzc96jwyo50gxffs853ae','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-06-19 02:26:43');

/*Table structure for table `django_site` */

DROP TABLE IF EXISTS `django_site`;

CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `django_site` */

insert  into `django_site`(`id`,`domain`,`name`) values (1,'example.com','example.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
