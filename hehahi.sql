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
CREATE DATABASE /*!32312 IF NOT EXISTS*/`devicemgtdb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `devicemgtdb`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=latin1;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add k_class',8,'add_k_class'),(23,'Can change k_class',8,'change_k_class'),(24,'Can delete k_class',8,'delete_k_class'),(25,'Can add k_purview',9,'add_k_purview'),(26,'Can change k_purview',9,'change_k_purview'),(27,'Can delete k_purview',9,'delete_k_purview'),(28,'Can add k_role',10,'add_k_role'),(29,'Can change k_role',10,'change_k_role'),(30,'Can delete k_role',10,'delete_k_role'),(31,'Can add k_classrole',11,'add_k_classrole'),(32,'Can change k_classrole',11,'change_k_classrole'),(33,'Can delete k_classrole',11,'delete_k_classrole'),(34,'Can add k_user',12,'add_k_user'),(35,'Can change k_user',12,'change_k_user'),(36,'Can delete k_user',12,'delete_k_user'),(37,'Can add k_devicetype',13,'add_k_devicetype'),(38,'Can change k_devicetype',13,'change_k_devicetype'),(39,'Can delete k_devicetype',13,'delete_k_devicetype'),(40,'Can add k_supplier',14,'add_k_supplier'),(41,'Can change k_supplier',14,'change_k_supplier'),(42,'Can delete k_supplier',14,'delete_k_supplier'),(43,'Can add k_producer',15,'add_k_producer'),(44,'Can change k_producer',15,'change_k_producer'),(45,'Can delete k_producer',15,'delete_k_producer'),(46,'Can add k_spare',16,'add_k_spare'),(47,'Can change k_spare',16,'change_k_spare'),(48,'Can delete k_spare',16,'delete_k_spare'),(49,'Can add k_device',17,'add_k_device'),(50,'Can change k_device',17,'change_k_device'),(51,'Can delete k_device',17,'delete_k_device'),(52,'Can add k_form',18,'add_k_form'),(53,'Can change k_form',18,'change_k_form'),(54,'Can delete k_form',18,'delete_k_form'),(55,'Can add k_formitem',19,'add_k_formitem'),(56,'Can change k_formitem',19,'change_k_formitem'),(57,'Can delete k_formitem',19,'delete_k_formitem'),(58,'Can add k_route',20,'add_k_route'),(59,'Can change k_route',20,'change_k_route'),(60,'Can delete k_route',20,'delete_k_route'),(61,'Can add k_meter',21,'add_k_meter'),(62,'Can change k_meter',21,'change_k_meter'),(63,'Can delete k_meter',21,'delete_k_meter'),(64,'Can add k_maintenance',22,'add_k_maintenance'),(65,'Can change k_maintenance',22,'change_k_maintenance'),(66,'Can delete k_maintenance',22,'delete_k_maintenance'),(67,'Can add k_task',23,'add_k_task'),(68,'Can change k_task',23,'change_k_task'),(69,'Can delete k_task',23,'delete_k_task'),(70,'Can add k_taskitem',24,'add_k_taskitem'),(71,'Can change k_taskitem',24,'change_k_taskitem'),(72,'Can delete k_taskitem',24,'delete_k_taskitem'),(73,'Can add k_sparebill',25,'add_k_sparebill'),(74,'Can change k_sparebill',25,'change_k_sparebill'),(75,'Can delete k_sparebill',25,'delete_k_sparebill'),(76,'Can add k_sparecount',26,'add_k_sparecount'),(77,'Can change k_sparecount',26,'change_k_sparecount'),(78,'Can delete k_sparecount',26,'delete_k_sparecount'),(79,'Can add k_tool',27,'add_k_tool'),(80,'Can change k_tool',27,'change_k_tool'),(81,'Can delete k_tool',27,'delete_k_tool'),(82,'Can add k_tooluse',28,'add_k_tooluse'),(83,'Can change k_tooluse',28,'change_k_tooluse'),(84,'Can delete k_tooluse',28,'delete_k_tooluse'),(85,'Can add k_toolcount',29,'add_k_toolcount'),(86,'Can change k_toolcount',29,'change_k_toolcount'),(87,'Can delete k_toolcount',29,'delete_k_toolcount'),(88,'Can add k_project',30,'add_k_project'),(89,'Can change k_project',30,'change_k_project'),(90,'Can delete k_project',30,'delete_k_project'),(91,'Can add k_schedule',31,'add_k_schedule'),(92,'Can change k_schedule',31,'change_k_schedule'),(93,'Can delete k_schedule',31,'delete_k_schedule'),(94,'Can add k_staffworkinfo',32,'add_k_staffworkinfo'),(95,'Can change k_staffworkinfo',32,'change_k_staffworkinfo'),(96,'Can delete k_staffworkinfo',32,'delete_k_staffworkinfo'),(97,'Can add k_staffscoreinfo',33,'add_k_staffscoreinfo'),(98,'Can change k_staffscoreinfo',33,'change_k_staffscoreinfo'),(99,'Can delete k_staffscoreinfo',33,'delete_k_staffscoreinfo'),(100,'Can add k_staffegginfo',34,'add_k_staffegginfo'),(101,'Can change k_staffegginfo',34,'change_k_staffegginfo'),(102,'Can delete k_staffegginfo',34,'delete_k_staffegginfo'),(103,'Can add k_feedback',35,'add_k_feedback'),(104,'Can change k_feedback',35,'change_k_feedback'),(105,'Can delete k_feedback',35,'delete_k_feedback');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values (1,'pbkdf2_sha256$12000$zye9t9QdSEaG$M8Fni5SGTy5+XB+u3H/eJwwlb3CCHZzw7ZdfuPeX9kE=','2015-04-13 12:18:19',1,'hahehi','','','hhyysbg@163.com',1,1,'2015-04-12 13:44:28');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_class` */

insert  into `devicemgt_k_class`(`id`,`parentid`,`depth`,`depthname`,`name`,`code`,`logo`,`address`,`zipcode`,`phone`,`license`,`licensetype`,`content`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,0,0,'WDYK company','WDYK company','','','','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00','');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_classrole` */

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
  `lastmaintenance` date NOT NULL,
  `nextmaintenance` date NOT NULL,
  `maintenanceperiod` int(10) unsigned NOT NULL,
  `lastrepaire` date NOT NULL,
  `lastmeter` date NOT NULL,
  `notice` varchar(100) NOT NULL,
  `ownerid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_device_432947aa` (`classid_id`),
  KEY `devicemgt_k_device_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_device_3f5d477e` (`typeid_id`),
  KEY `devicemgt_k_device_69308dea` (`supplierid_id`),
  CONSTRAINT `classid_id_refs_id_e8134469` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_0ca0a6d9` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_b397bc4d` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`),
  CONSTRAINT `typeid_id_refs_id_33dcc1e6` FOREIGN KEY (`typeid_id`) REFERENCES `devicemgt_k_devicetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_device` */

insert  into `devicemgt_k_device`(`id`,`classid_id`,`brand`,`producerid_id`,`typeid_id`,`supplierid_id`,`state`,`name`,`brief`,`serial`,`model`,`buytime`,`content`,`qrcode`,`position`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`,`lastmaintenance`,`nextmaintenance`,`maintenanceperiod`,`lastrepaire`,`lastmeter`,`notice`,`ownerid`) values (1,1,'',1,1,1,'0','111','111','11111','','0000-00-00','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00','','0000-00-00','0000-00-00',0,'0000-00-00','0000-00-00','',0);

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_device_spare` */

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_devicetype` */

insert  into `devicemgt_k_devicetype`(`id`,`parentid`,`depth`,`name`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,0,0,'','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00','');

/*Table structure for table `devicemgt_k_feedback` */

DROP TABLE IF EXISTS `devicemgt_k_feedback`;

CREATE TABLE `devicemgt_k_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(200) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_feedback` */

/*Table structure for table `devicemgt_k_form` */

DROP TABLE IF EXISTS `devicemgt_k_form`;

CREATE TABLE `devicemgt_k_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `period` int(10) unsigned NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_form` */

/*Table structure for table `devicemgt_k_formitem` */

DROP TABLE IF EXISTS `devicemgt_k_formitem`;

CREATE TABLE `devicemgt_k_formitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `formid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `threshold` varchar(30) NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_formitem` */

/*Table structure for table `devicemgt_k_maintenance` */

DROP TABLE IF EXISTS `devicemgt_k_maintenance`;

CREATE TABLE `devicemgt_k_maintenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `createcontent` varchar(100) NOT NULL,
  `editcontent` varchar(100) NOT NULL,
  `auditcontent` varchar(100) NOT NULL,
  `image` varchar(30) NOT NULL,
  `factor` int(10) unsigned NOT NULL,
  `memo` varchar(100) NOT NULL,
  `mtype` varchar(1) NOT NULL,
  `priority` varchar(1) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_maintenance_72537f95` (`deviceid_id`),
  CONSTRAINT `deviceid_id_refs_id_e790c6dd` FOREIGN KEY (`deviceid_id`) REFERENCES `devicemgt_k_device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_maintenance` */

/*Table structure for table `devicemgt_k_meter` */

DROP TABLE IF EXISTS `devicemgt_k_meter`;

CREATE TABLE `devicemgt_k_meter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` varchar(100) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_meter_72537f95` (`deviceid_id`),
  CONSTRAINT `deviceid_id_refs_id_ff1ae68d` FOREIGN KEY (`deviceid_id`) REFERENCES `devicemgt_k_device` (`id`)
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_producer` */

insert  into `devicemgt_k_producer`(`id`,`name`,`contact`,`addr`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`) values (1,'','','','',0,'0000-00-00',0,'0000-00-00');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_purview` */

insert  into `devicemgt_k_purview`(`id`,`classid_id`,`name`,`item`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'class','view','such as companies, departments, teams',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(2,1,'class','add','such as companies, departments, teams',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(4,1,'class','edit','such as companies, departments, teams',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(5,1,'class','delete','such as companies, departments, teams',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(6,1,'class','audit','such as companies, departments, teams',1,'0000-00-00',1,'0000-00-00',1,'0000-00-00','3'),(7,1,'role','view','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(8,1,'role','add','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(9,1,'role','edit','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(10,1,'role','delete','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(11,1,'user','view','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00',''),(12,1,'user','add','such as...',1,'0000-00-00',1,'0000-00-00',0,'0000-00-00','');

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_role` */

insert  into `devicemgt_k_role`(`id`,`classid_id`,`name`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`) values (1,1,'purview_design','312',1,'2015-04-07',1,'2015-04-15',1,'2015-04-15','3'),(2,1,'information_audition','31232',1,'2015-04-15',1,'2015-04-15',1,'2015-04-17','3');

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_role_purviews` */

insert  into `devicemgt_k_role_purviews`(`id`,`k_role_id`,`k_purview_id`) values (2,1,1),(3,1,2),(4,1,5),(5,1,7),(6,2,1),(9,2,6),(7,2,8),(8,2,10);

/*Table structure for table `devicemgt_k_route` */

DROP TABLE IF EXISTS `devicemgt_k_route`;

CREATE TABLE `devicemgt_k_route` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `formid` varchar(80) NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_route` */

/*Table structure for table `devicemgt_k_schedule` */

DROP TABLE IF EXISTS `devicemgt_k_schedule`;

CREATE TABLE `devicemgt_k_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `range` varchar(30) NOT NULL,
  `content` varchar(500) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_schedule_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_4dc8fa60` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_schedule` */

/*Table structure for table `devicemgt_k_spare` */

DROP TABLE IF EXISTS `devicemgt_k_spare`;

CREATE TABLE `devicemgt_k_spare` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `brand` varchar(30) NOT NULL,
  `producerid_id` int(11) NOT NULL,
  `typeid_id` int(11) NOT NULL,
  `model` varchar(30) NOT NULL,
  `supplierid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `minimum` int(10) unsigned NOT NULL,
  `stock` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  `ownerid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_spare_432947aa` (`classid_id`),
  KEY `devicemgt_k_spare_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_spare_3f5d477e` (`typeid_id`),
  KEY `devicemgt_k_spare_69308dea` (`supplierid_id`),
  CONSTRAINT `classid_id_refs_id_0b558ac8` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_9fd74a5a` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_b2e6caa3` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`),
  CONSTRAINT `typeid_id_refs_id_a440dc6f` FOREIGN KEY (`typeid_id`) REFERENCES `devicemgt_k_devicetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_spare` */

/*Table structure for table `devicemgt_k_sparebill` */

DROP TABLE IF EXISTS `devicemgt_k_sparebill`;

CREATE TABLE `devicemgt_k_sparebill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_sparebill_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_4ffbefc7` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_sparebill` */

/*Table structure for table `devicemgt_k_sparecount` */

DROP TABLE IF EXISTS `devicemgt_k_sparecount`;

CREATE TABLE `devicemgt_k_sparecount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `billid_id` int(11) NOT NULL,
  `deviceid_id` int(11) NOT NULL,
  `spareid_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_sparecount_fffd73c7` (`billid_id`),
  KEY `devicemgt_k_sparecount_72537f95` (`deviceid_id`),
  KEY `devicemgt_k_sparecount_12fc9209` (`spareid_id`),
  CONSTRAINT `billid_id_refs_id_175e7a4d` FOREIGN KEY (`billid_id`) REFERENCES `devicemgt_k_sparebill` (`id`),
  CONSTRAINT `deviceid_id_refs_id_26f51343` FOREIGN KEY (`deviceid_id`) REFERENCES `devicemgt_k_device` (`id`),
  CONSTRAINT `spareid_id_refs_id_c63e4168` FOREIGN KEY (`spareid_id`) REFERENCES `devicemgt_k_spare` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  `state` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_staffegginfo_936913d1` (`userid_id`),
  CONSTRAINT `userid_id_refs_id_95587539` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_staffegginfo` */

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_staffscoreinfo` */

/*Table structure for table `devicemgt_k_staffworkinfo` */

DROP TABLE IF EXISTS `devicemgt_k_staffworkinfo`;

CREATE TABLE `devicemgt_k_staffworkinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid_id` int(11) NOT NULL,
  `checkin` date NOT NULL,
  `checkout` date NOT NULL,
  `shifting` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_staffworkinfo_936913d1` (`userid_id`),
  CONSTRAINT `userid_id_refs_id_9174919c` FOREIGN KEY (`userid_id`) REFERENCES `devicemgt_k_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_supplier` */

insert  into `devicemgt_k_supplier`(`id`,`name`,`contact`,`addr`,`memo`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`) values (1,'','','','',0,'0000-00-00',0,'0000-00-00');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_task` */

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_taskitem` */

/*Table structure for table `devicemgt_k_tool` */

DROP TABLE IF EXISTS `devicemgt_k_tool`;

CREATE TABLE `devicemgt_k_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `brief` varchar(30) NOT NULL,
  `brand` varchar(30) NOT NULL,
  `producerid_id` int(11) NOT NULL,
  `typeid_id` int(11) NOT NULL,
  `model` varchar(30) NOT NULL,
  `supplierid_id` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `minimum` int(10) unsigned NOT NULL,
  `stock` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_tool_432947aa` (`classid_id`),
  KEY `devicemgt_k_tool_5c5fdea6` (`producerid_id`),
  KEY `devicemgt_k_tool_3f5d477e` (`typeid_id`),
  KEY `devicemgt_k_tool_69308dea` (`supplierid_id`),
  CONSTRAINT `classid_id_refs_id_67fdcf25` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`),
  CONSTRAINT `producerid_id_refs_id_1d6747ec` FOREIGN KEY (`producerid_id`) REFERENCES `devicemgt_k_producer` (`id`),
  CONSTRAINT `supplierid_id_refs_id_ea0efb3f` FOREIGN KEY (`supplierid_id`) REFERENCES `devicemgt_k_supplier` (`id`),
  CONSTRAINT `typeid_id_refs_id_3635e9d5` FOREIGN KEY (`typeid_id`) REFERENCES `devicemgt_k_devicetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_tool` */

/*Table structure for table `devicemgt_k_toolcount` */

DROP TABLE IF EXISTS `devicemgt_k_toolcount`;

CREATE TABLE `devicemgt_k_toolcount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `toolid_id` int(11) NOT NULL,
  `tooluseid_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `memo` varchar(100) NOT NULL,
  `stock` int(10) unsigned NOT NULL,
  `creatorid` int(10) unsigned NOT NULL,
  `createdatetime` date NOT NULL,
  `editorid` int(10) unsigned NOT NULL,
  `editdatetime` date NOT NULL,
  `auditorid` int(10) unsigned NOT NULL,
  `auditdatetime` date NOT NULL,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_toolcount_9e808b4a` (`toolid_id`),
  KEY `devicemgt_k_toolcount_b20c4629` (`tooluseid_id`),
  CONSTRAINT `toolid_id_refs_id_bf3b36c6` FOREIGN KEY (`toolid_id`) REFERENCES `devicemgt_k_tool` (`id`),
  CONSTRAINT `tooluseid_id_refs_id_b9a6ae2c` FOREIGN KEY (`tooluseid_id`) REFERENCES `devicemgt_k_tooluse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_toolcount` */

/*Table structure for table `devicemgt_k_tooluse` */

DROP TABLE IF EXISTS `devicemgt_k_tooluse`;

CREATE TABLE `devicemgt_k_tooluse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentid` int(10) unsigned NOT NULL,
  `toolid_id` int(11) NOT NULL,
  `number` int(10) unsigned NOT NULL,
  `ownerid` int(10) unsigned NOT NULL,
  `stock` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_tooluse_9e808b4a` (`toolid_id`),
  CONSTRAINT `toolid_id_refs_id_28000472` FOREIGN KEY (`toolid_id`) REFERENCES `devicemgt_k_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  PRIMARY KEY (`id`),
  KEY `devicemgt_k_user_432947aa` (`classid_id`),
  CONSTRAINT `classid_id_refs_id_6b588af6` FOREIGN KEY (`classid_id`) REFERENCES `devicemgt_k_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_user` */

insert  into `devicemgt_k_user`(`id`,`classid_id`,`state`,`username`,`password`,`name`,`face`,`mobile`,`email`,`address`,`zipcode`,`birthday`,`idcard`,`idcardtype`,`content`,`memo`,`contact`,`contactmobile`,`creatorid`,`createdatetime`,`editorid`,`editdatetime`,`auditorid`,`auditdatetime`,`status`,`todo`,`onlinetime`) values (1,1,'','hhy','hhy','','','','','','','0000-00-00','','','','','','',0,'0000-00-00',0,'0000-00-00',0,'0000-00-00','',0,0);

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `devicemgt_k_user_roles` */

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'k_class','devicemgt','k_class'),(9,'k_purview','devicemgt','k_purview'),(10,'k_role','devicemgt','k_role'),(11,'k_classrole','devicemgt','k_classrole'),(12,'k_user','devicemgt','k_user'),(13,'k_devicetype','devicemgt','k_devicetype'),(14,'k_supplier','devicemgt','k_supplier'),(15,'k_producer','devicemgt','k_producer'),(16,'k_spare','devicemgt','k_spare'),(17,'k_device','devicemgt','k_device'),(18,'k_form','devicemgt','k_form'),(19,'k_formitem','devicemgt','k_formitem'),(20,'k_route','devicemgt','k_route'),(21,'k_meter','devicemgt','k_meter'),(22,'k_maintenance','devicemgt','k_maintenance'),(23,'k_task','devicemgt','k_task'),(24,'k_taskitem','devicemgt','k_taskitem'),(25,'k_sparebill','devicemgt','k_sparebill'),(26,'k_sparecount','devicemgt','k_sparecount'),(27,'k_tool','devicemgt','k_tool'),(28,'k_tooluse','devicemgt','k_tooluse'),(29,'k_toolcount','devicemgt','k_toolcount'),(30,'k_project','devicemgt','k_project'),(31,'k_schedule','devicemgt','k_schedule'),(32,'k_staffworkinfo','devicemgt','k_staffworkinfo'),(33,'k_staffscoreinfo','devicemgt','k_staffscoreinfo'),(34,'k_staffegginfo','devicemgt','k_staffegginfo'),(35,'k_feedback','devicemgt','k_feedback');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values ('qnycv2lb6i7mymhaaemqbzaval2fl8h2','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-04-27 12:18:19'),('skw8slv7enk0sxdgzhacbp241p9amjbc','ZmFlYTJlMDA5NzA2MTQyNTZjNjUwMWFjNGViNDdiOTJkOGUwOTQ0ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-04-26 13:48:14');

/*Table structure for table `django_site` */

DROP TABLE IF EXISTS `django_site`;

CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `django_site` */

insert  into `django_site`(`id`,`domain`,`name`) values (1,'example.com','example.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
