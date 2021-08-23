CREATE DATABASE ecs;
USE ecs;
CREATE TABLE `status` (
    `id` INT UNSIGNED NOT NULL DEFAULT 1,
    `instance` VARCHAR(50),
    `last_updated` TIMESTAMP NOT NULL,
    `ip` VARCHAR(30)
);
CREATE TABLE history (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `created_by` VARCHAR(20) NOT NULL,
    `instance` VARCHAR(50),
    `action` VARCHAR(10) NOT NULL
);
CREATE TABLE cmd_history (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `created_by` VARCHAR(20) NOT NULL,
    `command_id` VARCHAR(50) NOT NULL,
    `invocation_id` VARCHAR(50) NOT NULL
);
INSERT INTO `status` () VALUES ();
CREATE DATABASE user;
USE user;
CREATE TABLE `data` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `last_updated` TIMESTAMP NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `password` VARCHAR(200) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `group` VARCHAR(10) NOT NULL,
    `nickname` VARCHAR(20) DEFAULT NULL
);