# Install and set up mysql database

import os.path

# Check if the config file exists
if(os.path.isfile(os.path.dirname(os.path.abspath(__file__))+"/web/config.py")== False):
	print("Please create the file web\\config.py before start installation")
	exit()

import web.config
import pymysql.cursors

print("Port listen: "+str(web.config.port_listen))

db = pymysql.connect(host=web.config.mysql_address, 
	user=web.config.mysql_user, 
	password=web.config.mysql_password, 
	charset="utf8mb4", 
	db=web.config.mysql_db, 
	cursorclass=pymysql.cursors.DictCursor)

try:

    with db.cursor() as cursor:
        # Read a single record
        sql = "SHOW TABLES;;"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

        # Create User information database
        sql = """CREATE TABLE IF NOT EXISTS `game_user`(
`user_id` INT(10) PRIMARY KEY AUTO_INCREMENT,
`username` VARCHAR(32) UNIQUE KEY NOT NULL,
`password` VARCHAR(128) NOT NULL, 
`nickname` VARCHAR(128), 
`email` VARCHAR(128), 
`reg_datetime` DATETIME, 
`description` TEXT
);"""
        cursor.execute(sql)

        # Create login information table
        sql = """CREATE TABLE IF NOT EXISTS `game_login`(
        `login_id` INT(50) PRIMARY KEY AUTO_INCREMENT,
        `user_id` INT(10) NOT NULL,
        `login_datetime` TIMESTAMP,
        `login_ip` VARCHAR(128), 
        `token` VARCHAR(128) NOT NULL,
        `expire_datetime` DATETIME NOT NULL,
        `enable` INT(5), 
        KEY `user_id`(`user_id`)
        )"""
        cursor.execute(sql)

        # Create game room database
        sql = """CREATE TABLE IF NOT EXISTS `game_room`(
        `auto_id` INT(50) PRIMARY KEY AUTO_INCREMENT,
        `room_id` INT(50) UNIQUE KEY NOT NULL,
        `holder` VARCHAR(32) NOT NULL,
        `game` VARCHAR(64) NOT NULL,
        `create_datetime` DATETIME,
        `room_stage` VARCHAR(32),
        `private_room` INT(4) DEFAULT 0,
        `guest` VARCHAR(32) DEFAULT NULL,
        `game_starttime` DATETIME,
        `permission` VARCHAR(128),
        KEY `holder` (`holder`), 
        KEY `permission` (`permission`)
        )"""
        cursor.execute(sql)

        # Create stage log of game room
        sql = """CREATE TABLE IF NOT EXISTS `game_roomstage`(
        `auto_stage_id` INT(50) PRIMARY KEY AUTO_INCREMENT,
        `room_id` INT(50) NOT NULL,
        `room_stage` VARCHAR(128) NOT NULL,
        `username` VARCHAR(32) DEFAULT NULL,
        `event_datetime` DATETIME, 
        KEY `room_id` (`room_id`)
        )"""
        cursor.execute(sql)

        # Create connect 4 game board
        sql = """CREATE TABLE IF NOT EXISTS `game_connect4board`(
        `step_id` INT(50) PRIMARY KEY AUTO_INCREMENT,
        `username` VARCHAR(32) NOT NULL,
        `game_side` INT(4) NOT NULL,
        `room_id` INT(50) NOT NULL,
        `row` INT(10) NOT NULL,
        `column` INT(10) NOT NULL,
        `move_time` DATETIME, 
        KEY `room_id` (`room_id`)
        )"""
        cursor.execute(sql)

        # Create table to store the game result
        sql = """CREATE TABLE IF NOT EXISTS `game_gameresult`(
        `record_id` INT(50) PRIMARY KEY AUTO_INCREMENT,
        `username` VARCHAR(32) NOT NULL,
        `room_id` INT(50) NOT NULL,
        `holder` VARCHAR(32) NOT NULL,
        `result` INT(10) NOT NULL,
        `total_step` INT(10) NOT NULL,
        `total_time` INT(20), 
        KEY `username` (`username`)
        )"""
        cursor.execute(sql)
finally:
    db.close()
    print("Finish installation")
