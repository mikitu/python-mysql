CREATE TABLE `happy_minute` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(5) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;