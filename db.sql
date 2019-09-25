use thecomics;
drop table IF EXISTS ITALIANCOMICS;
drop table IF EXISTS AMERICANCOMICS;

CREATE TABLE ITALIANCOMICS
( serie_title VARCHAR(600),
  link_albo VARCHAR(600),
  serie_year INTEGER,
  serie_numbers VARCHAR(600),
  publisher VARCHAR(600),
  issue_title VARCHAR(600),
  issue_originalstories VARCHAR(2083),
  issue_subtitle VARCHAR(600),
  issue_date DATE,
  issue_description VARCHAR(2083),
  issue_link_image VARCHAR(2083));

CREATE TABLE AMERICANCOMICS
( serie_title VARCHAR(600),
  link_albo VARCHAR(600),
  serie_year INTEGER,
  serie_numbers VARCHAR(600),
  publisher VARCHAR(600),
  issue_title VARCHAR(600),
  issue_originalstories VARCHAR(2083),
  issue_subtitle VARCHAR(600),
  issue_date DATE,
  issue_description VARCHAR(2083),
  issue_link_image VARCHAR(2083));

SET @@global.time_zone = '+02:00';
SET @@session.time_zone = '+02:00';