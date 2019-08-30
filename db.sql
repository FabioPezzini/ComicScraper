use italiancomics;
drop table IF EXISTS PANINICOMICS;
CREATE TABLE PANINICOMICS
( title VARCHAR(600),
  link VARCHAR(2083),
  subtitle VARCHAR(600),
  series VARCHAR(2083),
  price VARCHAR(600),
  pub_date DATE,
  include VARCHAR(2083),
  authors VARCHAR(2083),
  image_url VARCHAR(2083),
  description VARCHAR(2083),
  pages VARCHAR(200));

SET @@global.time_zone = '+02:00';
SET @@session.time_zone = '+02:00';