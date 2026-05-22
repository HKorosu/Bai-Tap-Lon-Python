CREATE DATABASE IF NOT EXISTS `news_management` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `news_management`;

CREATE TABLE IF NOT EXISTS `categories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `sources` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `source_name` VARCHAR(255) NOT NULL,
  `url` VARCHAR(512) NOT NULL,
  `category_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `articles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `source_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `title` VARCHAR(512) NOT NULL,
  `url` VARCHAR(512) NOT NULL UNIQUE,
  `summary` TEXT,
  `content` MEDIUMTEXT,
  `status` TINYINT NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`source_id`) REFERENCES `sources`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO `categories` (`name`) VALUES
('Công nghệ'),
('Kinh doanh'),
('Thể thao'),
('Giải trí'),
('Xã hội');

-- Source mẫu để demo (nếu bạn muốn dùng ngay):
INSERT IGNORE INTO `sources` (`source_name`, `url`, `category_id`) VALUES
('VnExpress - Công nghệ', 'https://vnexpress.net/tin-tuc-so-hoa', 1),
('Tuổi Trẻ - Kinh doanh', 'https://tuoitre.vn/kinh-doanh.htm', 2);
