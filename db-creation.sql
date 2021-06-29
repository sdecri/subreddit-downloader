drop database if exists reddit;
create database reddit;

use reddit;
drop table if exists subreddit;
CREATE TABLE subreddit (
  id varchar(255),
  name varchar(255),
  display_name varchar(255),
  title varchar(255),
  created_utc bigint,
  PRIMARY KEY (id)
);

drop table if exists submission;
CREATE TABLE submission (
  id varchar(255),
  subreddit varchar(255),
  created_utc bigint,
  score int,
  title varchar(255),  
  num_comments int,
  permalink varchar(255),
  url varchar(255),
  PRIMARY KEY (id),
  FOREIGN KEY (subreddit) REFERENCES subreddit(id)
);

drop table if exists comment;
CREATE TABLE comment (
  id varchar(255),
  submission varchar(255),
  created_utc bigint,
  score int,
  body text,
  permalink varchar(255),
  PRIMARY KEY (id),
  FOREIGN KEY (submission) REFERENCES submission(id)
);


