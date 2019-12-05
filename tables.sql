use nam;
create table if not exists Users(
	user varchar(32) NOT NULL,
	pass varchar(32) NOT NULL,
	id varchar(1 NOT NULL),
	PRIMARY KEY (user)
);

create table news(
	id int auto_increment,
	title varchar(32),
	news varchar(500),
	user_id varchar(32),
	primary key (id),
	foreign key(user_id) references Users(user)

);
insert into Users(user, pass, id) values("admin", "admin", "b");