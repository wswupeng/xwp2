/*be careful! the data may be valueable!*/

DROP DATABASE blog2; 
CREATE DATABASE blog2;
USE blog2;

create table posts 
(
	id int not null auto_increment,
	author_id int not null,
	title text not null,
	content text not null,
	excerpt text,
	posted_on datetime not null default '0000-00-00 00:00:00',
	modified_on datetime not null default '0000-00-00 00:00:00',
	slug varchar(32) unique, 
	post_type varchar(32) not null default 'blog', /*blog, page,...*/
	comment_status varchar(32) not null default 'open', /*open means allow comment,close means not allow.*/
	post_status varchar(32) not null default 'published', /*published, publishing*/
	/*comment_count int default 0,*/

	primary key (id),
	foreign key (author_id) references users(id)
);

create table comments 
(
	id int not null auto_increment,
	post_id int not null,
	author varchar(32) not null,
	author_ip varchar(32) not null,
	content text not null,
	posted_on DATETIME not null,
	url text,
	email text,
	reply_notify_mail int not null,
	comment_agent varchar(32), /*firefox, chrome, ie,etc.*/
	
	primary key (id),
	foreign key (post_id) references posts(id)
);

/*
create table categories 
(
	id int auto_increment,
	name text not null,
	parent_id int default 0,
	description varchar(255) default '',
	primary key (id)
);

create table tags 
(
	id int auto_increment,
	name text not null,
	primary key (id)
);
*/

create table users 
(
	id int not null auto_increment,
	name varchar(32) unique not null,
	password text not null,
	priority text not null, /*admin, common.*/
	registered_on datetime not null default '0000-00-00 00:00:00',
	email text default '',
	url text default '',

	primary key (id)
);

create table uploads 
(
	id int not null auto_increment,
	file_name text not null,
	file_size int not null, 

	primary key (id)
);

/*global blog config info.*/
create table ginfo 
(
	id int not null auto_increment,
	title varchar(32) not null default 'XWP',
	subtitle varchar(32) default '',
	owner varchar(32) not null default '',
	baseurl varchar(255) not null default '', 
	feedurl varchar(255) not null default '/feed',
	post_count int not null default 0,
	post_per_page int not null default 10,
	version varchar(255) not null default "maybe this should put into config file, not the table.", 	
	comment_per_page int not null default 20,
	lang varchar(32) not null default 'en-us',
	
	primary key (id)
);

create table terms 
(
	id int not null auto_increment,
	name text not null,
	parent_id int not null default 0,
	description varchar(255) not null default '',
	type varchar(255) not null check(type in ('post_tag', 'post_category')), 
	primary key (id)
);

create table term_relationship
(
	post_id int not null,  
	term_id int not null, 
	term_type varchar(255) not null check(term_type in ('post_tag', 'post_category')), 

	primary key (post_id, term_id),
	foreign key (post_id) references posts(id),
	foreign key (term_id) references terms(id)
);

create table options
(
	is_custom int not null, /*0:system options, 1:custom options.*/
	name varchar(255) not null,
	value text not null,

	primary key (name)
);


/*TODO insert some basic data here.*/
insert into terms(name, parent_id, description, type) values ('uncategorized', 0, '', 'post_category');
insert into terms(name, parent_id, description, type) values ('NoneTag', 0, '', 'post_tag');

/*
	insert into option, global settings. 
	insert into options(is_custom, name, value) values(1, '', '')
*/
insert into options(is_custom, name, value) values(1, 'title', 'xwp');
insert into options(is_custom, name, value) values(1, 'subtitle', 'xwp');
insert into options(is_custom, name, value) values(1, 'notice', 'yes we can!');

/*?? should we decide it in */
insert into options(is_custom, name, value) values(1, 'baseurl', '//localhost:8080');
insert into options(is_custom, name, value) values(1, 'post_per_page', '10');
insert into options(is_custom, name, value) values(1, 'comment_per_page', '30');

/*
insert into posts
insert into users
*/
insert into users(name, password, priority) values('admin', 'bb798daca8bf1a25ee11559aa52b6c89', 'admin');
