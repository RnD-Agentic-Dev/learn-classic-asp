-- Fixture: seed known test data into tb_posts
-- Run this before the test suite to ensure a predictable starting state.

-- Clear any previous test data
DELETE FROM tb_posts WHERE title LIKE '__test_%';

-- Insert known test records
INSERT INTO tb_posts (title, content, status, deleted)
VALUES ('__test_post_1', 'Test content for post 1', 'published', 'N');

INSERT INTO tb_posts (title, content, status, deleted)
VALUES ('__test_post_2', 'Test content for post 2', 'draft', 'N');

INSERT INTO tb_posts (title, content, status, deleted)
VALUES ('__test_deleted_post', 'This post is soft-deleted', 'published', 'Y');
