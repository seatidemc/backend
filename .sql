CREATE DATABASE ecs_central;
USE ecs_central;
CREATE TABLE ecs_status (
    `id` INT UNSIGNED NOT NULL DEFAULT 1,
    `instance` VARCHAR(50),
    `last_updated` TIMESTAMP NOT NULL
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
INSERT INTO ecs_status () VALUES ();