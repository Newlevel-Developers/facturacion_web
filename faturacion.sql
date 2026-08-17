/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.23-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: facturacion
-- ------------------------------------------------------
-- Server version	10.6.23-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add producto',7,'add_producto'),(26,'Can change producto',7,'change_producto'),(27,'Can delete producto',7,'delete_producto'),(28,'Can view producto',7,'view_producto'),(29,'Can add categoria',8,'add_categoria'),(30,'Can change categoria',8,'change_categoria'),(31,'Can delete categoria',8,'delete_categoria'),(32,'Can view categoria',8,'view_categoria'),(33,'Can add detalle factura',9,'add_detallefactura'),(34,'Can change detalle factura',9,'change_detallefactura'),(35,'Can delete detalle factura',9,'delete_detallefactura'),(36,'Can view detalle factura',9,'view_detallefactura'),(37,'Can add factura',10,'add_factura'),(38,'Can change factura',10,'change_factura'),(39,'Can delete factura',10,'delete_factura'),(40,'Can view factura',10,'view_factura'),(41,'Can add cliente',11,'add_cliente'),(42,'Can change cliente',11,'change_cliente'),(43,'Can delete cliente',11,'delete_cliente'),(44,'Can view cliente',11,'view_cliente'),(45,'Can add tipo_documnento',12,'add_tipo_documnento'),(46,'Can change tipo_documnento',12,'change_tipo_documnento'),(47,'Can delete tipo_documnento',12,'delete_tipo_documnento'),(48,'Can view tipo_documnento',12,'view_tipo_documnento');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$u7OHnlBfJlFeo3Xye3uryx$Zh2lDpv2RRqGAvDhO0jv/sv90QcAKF1YS7DsYvsLYF4=','2026-03-11 15:44:19.006423',1,'manuel','luis','navarro','manuel@gmail.com',1,1,'2026-03-09 15:37:25.694800'),(2,'pbkdf2_sha256$600000$lBmoNip0l8r16qX3TbAhYx$Xe5UrQvA3VUHOPAOoYdhSPU4KGzLdFDt4snGLBProMs=',NULL,0,'lnavarro','manuel','navarro','lnavarro@mercal.gob.ve',0,1,'2026-03-09 18:54:04.942038'),(3,'pbkdf2_sha256$600000$U8dWA2bvs4HdwYewTc2uIh$YYB/rp6b9leNAi/VraZ3f6mDVjMXpDQLR482AZROj5c=',NULL,0,'lmoreno','moises','miranda','lnavarro@mercal.gob.ve',0,1,'2026-03-11 15:53:03.869534');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_cliente`
--

DROP TABLE IF EXISTS `clientes_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_cliente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tipo_documento_id` varchar(3) NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `direccion` longtext NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_cliente`
--

LOCK TABLES `clientes_cliente` WRITE;
/*!40000 ALTER TABLE `clientes_cliente` DISABLE KEYS */;
INSERT INTO `clientes_cliente` VALUES (1,'1','31158004','luis','navarro','lm395746@gmail.com','04241871113','antimano','2025-06-11 12:10:44.000000',1),(2,'1','31158004','manuel navarro','','lnavarro@mercal.gob.ve','04247703339','antimano','2026-03-11 17:20:41.058823',0),(3,'1','31158004','morneo','','lnavarro@mercal.gob.ve','04247703339','caracas','2026-03-11 17:21:24.884324',0),(4,'2','31158004','dan','','admin@gmail.com','04247703339','antimano','2026-03-11 17:21:54.669609',0),(5,'1','31158005','manuel navarro','','lnavarro@mercal.gob.ve','04247703339','caracas','2026-03-11 17:25:02.465083',1);
/*!40000 ALTER TABLE `clientes_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'facturacion','categoria'),(11,'facturacion','cliente'),(9,'facturacion','detallefactura'),(10,'facturacion','factura'),(7,'facturacion','producto'),(12,'facturacion','tipo_documnento'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-06 19:59:40.338126'),(2,'auth','0001_initial','2026-03-06 19:59:43.813212'),(3,'admin','0001_initial','2026-03-06 19:59:44.513142'),(4,'admin','0002_logentry_remove_auto_add','2026-03-06 19:59:44.543882'),(5,'admin','0003_logentry_add_action_flag_choices','2026-03-06 19:59:44.573789'),(6,'contenttypes','0002_remove_content_type_name','2026-03-06 19:59:45.071360'),(7,'auth','0002_alter_permission_name_max_length','2026-03-06 19:59:45.337982'),(8,'auth','0003_alter_user_email_max_length','2026-03-06 19:59:45.521111'),(9,'auth','0004_alter_user_username_opts','2026-03-06 19:59:45.552167'),(10,'auth','0005_alter_user_last_login_null','2026-03-06 19:59:45.788009'),(11,'auth','0006_require_contenttypes_0002','2026-03-06 19:59:45.808136'),(12,'auth','0007_alter_validators_add_error_messages','2026-03-06 19:59:45.826857'),(13,'auth','0008_alter_user_username_max_length','2026-03-06 19:59:45.988064'),(14,'auth','0009_alter_user_last_name_max_length','2026-03-06 19:59:46.154652'),(15,'auth','0010_alter_group_name_max_length','2026-03-06 19:59:46.446398'),(16,'auth','0011_update_proxy_permissions','2026-03-06 19:59:46.477605'),(17,'auth','0012_alter_user_first_name_max_length','2026-03-06 19:59:46.629850'),(18,'sessions','0001_initial','2026-03-06 19:59:46.937947'),(19,'facturacion','0001_initial','2026-03-06 20:07:48.771989'),(20,'facturacion','0002_tipo_documnento_alter_cliente_tipo_documento','2026-03-11 16:35:25.978461');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('pvvlrs7flsnnjuoh55q8zkdkbzby3p6b','.eJxVjMsOwiAQRf-FtSG8B1y69xvIlAGpGkhKuzL-uzbpQrf3nHNfLOK21riNvMSZ2JlJdvrdJkyP3HZAd2y3zlNv6zJPfFf4QQe_dsrPy-H-HVQc9Vuj18lqW7wFQG_IB5OtBgABpCG4IpGcFcFJlXzGQEq4oItNpgBKFdj7A7yrNt0:1vzcfz:0f75k9h3WTbkcRC9q15yrI_FWv58ZNzlU8kVPWox238','2026-03-23 15:37:47.711532'),('wsjw1jce87zc0acvyobkumxlau1797dq','.eJxVjMsOwiAQRf-FtSG8B1y69xvIlAGpGkhKuzL-uzbpQrf3nHNfLOK21riNvMSZ2JlJdvrdJkyP3HZAd2y3zlNv6zJPfFf4QQe_dsrPy-H-HVQc9Vuj18lqW7wFQG_IB5OtBgABpCG4IpGcFcFJlXzGQEq4oItNpgBKFdj7A7yrNt0:1w0LjP:fUNv9k_WrGOW1XWPDTwfNfgKQgUXl3PYpsx24hTK-HE','2026-03-25 15:44:19.019282');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturas_detallefactura`
--

DROP TABLE IF EXISTS `facturas_detallefactura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturas_detallefactura` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `factura_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facturas_detallefact_factura_id_005f9223_fk_facturas_` (`factura_id`),
  KEY `facturas_detallefact_producto_id_988566c5_fk_productos` (`producto_id`),
  CONSTRAINT `facturas_detallefact_factura_id_005f9223_fk_facturas_` FOREIGN KEY (`factura_id`) REFERENCES `facturas_factura` (`id`),
  CONSTRAINT `facturas_detallefact_producto_id_988566c5_fk_productos` FOREIGN KEY (`producto_id`) REFERENCES `productos_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturas_detallefactura`
--

LOCK TABLES `facturas_detallefactura` WRITE;
/*!40000 ALTER TABLE `facturas_detallefactura` DISABLE KEYS */;
/*!40000 ALTER TABLE `facturas_detallefactura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturas_factura`
--

DROP TABLE IF EXISTS `facturas_factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturas_factura` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `numero_factura` varchar(20) NOT NULL,
  `tipo_comprobante` varchar(10) NOT NULL,
  `fecha_emision` datetime(6) NOT NULL,
  `fecha_pago` datetime(6) DEFAULT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `igv` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facturas_factura_cliente_id_c7ebc781_fk_clientes_cliente_id` (`cliente_id`),
  KEY `facturas_factura_usuario_id_2269c3b8_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `facturas_factura_cliente_id_c7ebc781_fk_clientes_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`),
  CONSTRAINT `facturas_factura_usuario_id_2269c3b8_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturas_factura`
--

LOCK TABLES `facturas_factura` WRITE;
/*!40000 ALTER TABLE `facturas_factura` DISABLE KEYS */;
/*!40000 ALTER TABLE `facturas_factura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_categoria`
--

DROP TABLE IF EXISTS `productos_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_categoria` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_categoria`
--

LOCK TABLES `productos_categoria` WRITE;
/*!40000 ALTER TABLE `productos_categoria` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_producto`
--

DROP TABLE IF EXISTS `productos_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_producto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `stock_minimo` int(11) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `categoria_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `productos_producto_categoria_id_1fef506a_fk_productos` (`categoria_id`),
  CONSTRAINT `productos_producto_categoria_id_1fef506a_fk_productos` FOREIGN KEY (`categoria_id`) REFERENCES `productos_categoria` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_producto`
--

LOCK TABLES `productos_producto` WRITE;
/*!40000 ALTER TABLE `productos_producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_documento`
--

DROP TABLE IF EXISTS `tipo_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_documento` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_documento`
--

LOCK TABLES `tipo_documento` WRITE;
/*!40000 ALTER TABLE `tipo_documento` DISABLE KEYS */;
INSERT INTO `tipo_documento` VALUES (1,'Venezolano'),(2,'Extranjero');
/*!40000 ALTER TABLE `tipo_documento` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-11 13:45:19
