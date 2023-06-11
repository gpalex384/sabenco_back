DROP schema IF EXISTS sabenco_back_test;
CREATE schema sabenco_back_test;
use sabenco_back_test;
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` varchar(36) NOT NULL DEFAULT uuid(),
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_un` (`name`),
  KEY `category_createdby_FK` (`createdby`),
  KEY `category_updatedby_FK` (`updatedby`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` varchar(36) NOT NULL DEFAULT uuid(),
  `name` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `updatedby` varchar(36) DEFAULT NULL,
  `createdby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_un` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `categoryrole`;
CREATE TABLE `categoryrole` (
  `category_id` varchar(36) NOT NULL,
  `role_id` varchar(36) NOT NULL,
  `active` tinyint(1) DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`category_id`,`role_id`),
  KEY `categorytype_createdby_FK` (`createdby`),
  KEY `categorytype_updatedby_FK` (`updatedby`),
  KEY `categoryrole_role_FK` (`role_id`),
  KEY `categoryrole_category_FK` (`category_id`),
  CONSTRAINT `categoryrole_category_FK` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `categoryrole_role_FK` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `event`;
CREATE TABLE `event` (
  `id` varchar(36) NOT NULL DEFAULT uuid(),
  `title` varchar(50) NOT NULL,
  `detail` text NOT NULL,
  `startdate` timestamp NOT NULL DEFAULT current_timestamp(),
  `enddate` timestamp NULL DEFAULT NULL,
  `category_id` varchar(36) DEFAULT NULL,
  `published` tinyint(1) NOT NULL DEFAULT 1,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_createdby_FK` (`createdby`),
  KEY `event_updatedby_FK` (`updatedby`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `eventcategory`;
CREATE TABLE `eventcategory` (
  `event_id` varchar(36) NOT NULL,
  `category_id` varchar(36) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`event_id`,`category_id`),
  KEY `eventcategory_category_fk` (`category_id`),
  CONSTRAINT `eventcategory_category_fk` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `eventcategory_event_fk` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `eventdraft`;
CREATE TABLE `eventdraft` (
  `id` varchar(36) NOT NULL DEFAULT 'uuid()',
  `event_id` varchar(36) DEFAULT NULL,
  `title` varchar(50) NOT NULL,
  `detail` text NOT NULL,
  `startdate` timestamp NOT NULL DEFAULT current_timestamp(),
  `enddate` timestamp NULL DEFAULT NULL,
  `pub_requested` tinyint(1) NOT NULL DEFAULT 0,
  `moderator_comment` text DEFAULT NULL,
  `published` tinyint(1) NOT NULL DEFAULT 0,
  `publishdate` timestamp NULL DEFAULT NULL,
  `obsolete` tinyint(1) NOT NULL DEFAULT 0,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `eventdraft_event_FK` (`event_id`),
  CONSTRAINT `eventdraft_event_FK` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `eventlink`;
CREATE TABLE `eventlink` (
  `event1_id` varchar(36) NOT NULL,
  `event2_id` varchar(36) NOT NULL,
  `link_description` text DEFAULT 'Description missing',
  `overseen` timestamp NULL DEFAULT NULL,
  `overseenby` varchar(36) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`event1_id`,`event2_id`),
  KEY `eventlink_event2_FK` (`event2_id`),
  KEY `eventlink_createdby_FK` (`createdby`),
  KEY `eventlink_updatedby_FK` (`updatedby`),
  KEY `eventlink_overseenby_FK` (`overseenby`),
  CONSTRAINT `eventlink_event1_FK` FOREIGN KEY (`event1_id`) REFERENCES `event` (`id`),
  CONSTRAINT `eventlink_event2_FK` FOREIGN KEY (`event2_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` varchar(36) NOT NULL DEFAULT uuid(),
  `username` varchar(50) NOT NULL,
  `usermail` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` varchar(100) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `createdby` varchar(36) DEFAULT NULL,
  `updatedby` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usermail_un` (`usermail`),
  UNIQUE KEY `user_un` (`username`),
  KEY `user_role_FK` (`role_id`),
  CONSTRAINT `user_role_FK` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4