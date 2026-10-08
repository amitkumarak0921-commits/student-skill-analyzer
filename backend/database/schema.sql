-- Generated from the SQLAlchemy models (MySQL 8). The API also creates these tables on first start.
CREATE DATABASE IF NOT EXISTS student_skill_analyzer CHARACTER SET utf8mb4;
USE student_skill_analyzer;

CREATE TABLE IF NOT EXISTS subjects (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(500) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);


CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	college VARCHAR(150), 
	branch VARCHAR(100), 
	semester VARCHAR(30), 
	`role` VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id)
);

CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE IF NOT EXISTS assessment_attempts (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	subject_id INTEGER NOT NULL, 
	level INTEGER NOT NULL, 
	session_id VARCHAR(64) NOT NULL, 
	total_questions INTEGER NOT NULL, 
	correct_answers INTEGER NOT NULL, 
	percentage NUMERIC(5, 2) NOT NULL, 
	passed BOOL NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(subject_id) REFERENCES subjects (id), 
	UNIQUE (session_id)
);

CREATE INDEX ix_assessment_attempts_subject_id ON assessment_attempts (subject_id);
CREATE INDEX ix_assessment_attempts_user_id ON assessment_attempts (user_id);

CREATE TABLE IF NOT EXISTS feedback (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	message TEXT NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_feedback_user_id ON feedback (user_id);

CREATE TABLE IF NOT EXISTS topics (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(100) NOT NULL, 
	subject_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_id) REFERENCES subjects (id)
);


CREATE TABLE IF NOT EXISTS questions (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	question_text VARCHAR(500) NOT NULL, 
	option_a VARCHAR(300) NOT NULL, 
	option_b VARCHAR(300) NOT NULL, 
	option_c VARCHAR(300) NOT NULL, 
	option_d VARCHAR(300) NOT NULL, 
	correct_answer VARCHAR(1) NOT NULL, 
	difficulty VARCHAR(20) NOT NULL, 
	topic_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(topic_id) REFERENCES topics (id)
);


CREATE TABLE IF NOT EXISTS user_answers (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	attempt_id INTEGER NOT NULL, 
	question_id INTEGER NOT NULL, 
	selected_answer VARCHAR(1) NOT NULL, 
	is_correct BOOL NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(attempt_id) REFERENCES assessment_attempts (id), 
	FOREIGN KEY(question_id) REFERENCES questions (id)
);

CREATE INDEX ix_user_answers_attempt_id ON user_answers (attempt_id);
