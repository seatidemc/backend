CREATE DATABASE ecs_central;
USE ecs_central;
CREATE TABLE ecs_status (
    `id` INT UNSIGNED NOT NULL DEFAULT 1,
    `status` VARCHAR(3) NOT NULL DEFAULT 'off',
    `last_updated` TIMESTAMP NOT NULL
);
CREATE TABLE history (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `status` VARCHAR(3) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `created_by` VARCHAR(20) NOT NULL
);
INSERT INTO ecs_status () VALUES ();