-- CREATE DATABASE users_db;
CREATE TABLE "user"
(
id serial,
username varchar(255),
email varchar(255) unique ,
hashed_password varchar (80),
PRIMARY KEY(id)
);
