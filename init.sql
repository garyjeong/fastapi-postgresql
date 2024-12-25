CREATE DATABASE test;
CREATE USER test_user WITH LOGIN PASSWORD 'test_user';
GRANT ALL PRIVILEGES ON DATABASE test TO test_user;

\c test;

GRANT ALL ON SCHEMA public TO test_user;

CREATE SCHEMA template_1;
GRANT ALL PRIVILEGES ON SCHEMA template_1 TO test_user;

CREATE SCHEMA template_2;
GRANT ALL PRIVILEGES ON SCHEMA template_2 TO test_user;

CREATE SCHEMA template_3;
GRANT ALL PRIVILEGES ON SCHEMA template_3 TO test_user;
