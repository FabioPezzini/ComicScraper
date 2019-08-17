use italiancomics;
CREATE TABLE PANINICOMICS
( title VARCHAR(2083),
  link VARCHAR(2083),
  subtitle VARCHAR(2083),
  series VARCHAR(2083),
  price DECIMAL(19,4),
  pub_date DATE,
  include VARCHAR(2083),
  authors VARCHAR(2083));

SET @@global.time_zone = '+02:00';
SET @@session.time_zone = '+02:00';