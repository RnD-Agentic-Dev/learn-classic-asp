-- Fixture: remove test data created during the test run.
-- Run this after the test suite to leave the database clean.

DELETE FROM tb_posts WHERE title LIKE '__test_%';
