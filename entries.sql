DROP DATABASE blog2; 
create database blog2;
use blog2;

CREATE TABLE entries (
		id INT AUTO_INCREMENT,
		title TEXT,
		content TEXT,
		posted_on DATETIME,
		slug TEXT,
		tag TEXT,
		categories TEXT, /*this field stories category id in table categories like '1,2,3,4,5'*/
		primary key (id)
		);

CREATE TABLE comments (
		id INT AUTO_INCREMENT,
		entry_id INT,
		author TEXT,
		content TEXT,
		posted_on DATETIME,
		url TEXT,
		email TEXT,
		reply_notify_mail INT,

		primary key (id),
		FOREIGN KEY (entry_id) REFERENCES entries(id)
		);

CREATE TABLE categories (
		id INT AUTO_INCREMENT,
		name TEXT,
		parent_id INT, 
		primary key (id)
		);


