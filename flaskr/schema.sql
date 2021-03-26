DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS cartoon;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  post_title TEXT NOT NULL,
  post_body TEXT NOT NULL,
  post_image TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (user_id)
);

CREATE TABLE comments (
  comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  commentor_id INTEGER NOT NULL,
  OG_post_id INTEGER NOT NULL,
  comment_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment_title TEXT NOT NULL,
  comment_body TEXT NOT NULL,
  FOREIGN KEY (OG_post_id) REFERENCES post (post_id)
);

CREATE TABLE cartoon (
  cartoon_id INTEGER PRIMARY KEY AUTOINCREMENT,
  cartoon_author_id INTEGER NOT NULL,
  cartoon_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cartoon_title TEXT NOT NULL,
  cartoon_original_image TEXT NOT NULL,
  cartoon_original_photo BLOB NOT NULL, 
  cartoon_image_name TEXT ,
  FOREIGN KEY (cartoon_author_id) REFERENCES user (user_id)
);
