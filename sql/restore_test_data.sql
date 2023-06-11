LOCK TABLES `category` WRITE;
INSERT INTO `category` VALUES 
('466ffe48-d3f1-11ed-b139-4ccc6a8143e6','myself','the category by default',1,'2023-04-05 20:34:32','2023-04-05 20:34:32',NULL,NULL),
('4670170a-d3f1-11ed-b139-4ccc6a8143e6','history','category for historic events',1,'2023-04-05 20:34:32','2023-04-05 20:34:32',NULL,NULL),
('46701cfe-d3f1-11ed-b139-4ccc6a8143e6','literature','category for literature events',1,'2023-04-05 20:34:32','2023-04-05 20:34:32',NULL,NULL),
('467c6d6e-d3f1-11ed-b139-4ccc6a8143e6','science','category for scientific events',1,'2023-04-05 20:34:32','2023-04-05 20:34:32',NULL,NULL);
UNLOCK TABLES;
LOCK TABLES `role` WRITE;
INSERT INTO `role` VALUES 
('2adab030-d4b4-11ed-b139-4ccc6a8143e6','registered',1,'2023-04-06 19:49:30','2023-04-06 19:49:30',NULL,NULL),
('2adc2b30-d4b4-11ed-b139-4ccc6a8143e6','editor',1,'2023-04-06 19:49:30','2023-04-06 19:49:30',NULL,NULL),
('2adc2be0-d4b4-11ed-b139-4ccc6a8143e6','moderator',1,'2023-04-06 19:49:30','2023-04-06 19:49:30',NULL,NULL),
('2adc2ca4-d4b4-11ed-b139-4ccc6a8143e6','admin',1,'2023-04-06 19:49:30','2023-04-06 19:49:30',NULL,NULL);
UNLOCK TABLES;
LOCK TABLES `categoryrole` WRITE;
INSERT INTO `categoryrole` VALUES 
('4670170a-d3f1-11ed-b139-4ccc6a8143e6', '2adab030-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- history - registered
('4670170a-d3f1-11ed-b139-4ccc6a8143e6', '2adc2b30-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- history - editor
('4670170a-d3f1-11ed-b139-4ccc6a8143e6', '2adc2be0-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- history - moderator
('4670170a-d3f1-11ed-b139-4ccc6a8143e6', '2adc2ca4-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- history - admin
('46701cfe-d3f1-11ed-b139-4ccc6a8143e6', '2adab030-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- literature - registered
('46701cfe-d3f1-11ed-b139-4ccc6a8143e6', '2adc2b30-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- literature - editor
('46701cfe-d3f1-11ed-b139-4ccc6a8143e6', '2adc2be0-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL), -- literature - moderator
('46701cfe-d3f1-11ed-b139-4ccc6a8143e6', '2adc2ca4-d4b4-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL); -- literature - admin
UNLOCK TABLES;
LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES 
('86224086-d4b5-11ed-b139-4ccc6a8143e6','admin1','user1@user','6c7ca345f63f835cb353ff15bd6c5e052ec08e7a','2adc2ca4-d4b4-11ed-b139-4ccc6a8143e6',1,'2023-04-06 19:59:13','2023-04-06 19:59:13',NULL,NULL);
UNLOCK TABLES;
LOCK TABLES `event` WRITE;
INSERT INTO `event` VALUES
('26f4e69f-014f-11ee-823e-4ccc6a8143e6', 'event title 1', 'event title 1 dummy details', current_timestamp(), NULL, NULL, 1, 1, current_timestamp(), current_timestamp(), NULL, NULL),
('26f4f246-014f-11ee-823e-4ccc6a8143e6', 'event title 2', 'event title 2 dummy details', '2023-04-15', NULL, NULL, 1, 1, current_timestamp(), current_timestamp(), NULL, NULL);
UNLOCK TABLES;
LOCK TABLES `eventcategory` WRITE;
INSERT INTO `eventcategory` VALUES
('26f4e69f-014f-11ee-823e-4ccc6a8143e6', '466ffe48-d3f1-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL),
('26f4f246-014f-11ee-823e-4ccc6a8143e6', '466ffe48-d3f1-11ed-b139-4ccc6a8143e6', 1, current_timestamp(), current_timestamp(), NULL, NULL);
UNLOCK TABLES