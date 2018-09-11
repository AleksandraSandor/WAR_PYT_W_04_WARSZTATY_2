CREATE DATABASE users_db;

CREATE TABLE "user"
(
id serial,
username varchar(255),
email varchar(255) unique ,
hashed_password varchar (80),
PRIMARY KEY(id)
);

create table message (
id serial,
from_id integer not null,
to_id integer not null,
text text,
creation_date timestamp,
primary key(id),
foreign key(from_id) REFERENCES "user"(id),
foreign key(to_id) REFERENCES "user"(id)
)