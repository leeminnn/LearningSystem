
CREATE DATABASE IF NOT EXISTS section;
CREATE TABLE IF NOT EXISTS section.section (
  section_id int NOT NULL,
  class_id int, 
  course_id int,
  section_name VARCHAR (255) NOT NULL,
  section_desc VARCHAR (255) NOT NULL,
  materials VARCHAR (255) NOT NULL,
  CONSTRAINT PK_section PRIMARY KEY (section_id, class_id, course_id)
);

CREATE TABLE IF NOT EXISTS section.quiz (
  quiz_id int NOT NULL PRIMARY KEY,
  section_id int,
  class_id int,
  course_id int,
  total_mark int NOT NULL, 
    FOREIGN KEY (section_id, class_id, course_id) REFERENCES section(section_id, class_id, course_id)
);

CREATE TABLE IF NOT EXISTS section.question (
  qn_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  quiz_id int,
  quiz_desc VARCHAR (255) NOT NULL,
  quiz_ans VARCHAR (255) NOT NULL,
  mark int NOT NULL, 
  CONSTRAINT question_fk_quiz FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);


CREATE DATABASE IF NOT EXISTS course;
CREATE TABLE course.course (
  course_id int NOT NULL PRIMARY KEY,
  course_name VARCHAR (255) NOT NULL,
  start_date date NOT NULL, 
  end_date date NOT NULL,
  pre_req VARCHAR (255) NOT NULL
);

CREATE TABLE IF NOT EXISTS course.class (
  class_id int NOT NULL PRIMARY KEY,
  class_name VARCHAR (255) NOT NULL,
  intake VARCHAR (255) NOT NULL,
  emp_id int, 
  course_id int,
  CONSTRAINT FK_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE IF NOT EXISTS course.class_list (
  emp_id int,
  class_id int,
  progress VARCHAR (255) NOT NULL,
  status VARCHAR (255) NOT NULL,
  CONSTRAINT PK_learner PRIMARY KEY (emp_id, class_id),
  CONSTRAINT learner_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE IF NOT EXISTS course.pending_enrolment (
  emp_id int,
  course_id int,
  class_id int,
  status VARCHAR (255) NOT NULL,
  CONSTRAINT pk_pending PRIMARY KEY (emp_id, class_id, course_id),
  CONSTRAINT pending_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT pending_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);


CREATE DATABASE IF NOT EXISTS employee;


-- add in heree
CREATE TABLE IF NOT EXISTS employee.employee (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255) NOT NULL,
  email VARCHAR (255) NOT NULL,
  phone int(8) NOT NULL,
  position VARCHAR (255) NOT NULL,
  dept VARCHAR (255) NOT NULL,
  course_complete VARCHAR (255) NOT NULL,
  badge VARCHAR (255) NOT NULL
);

DROP DATABASE IF EXISTS learningsystem;