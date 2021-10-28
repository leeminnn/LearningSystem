CREATE DATABASE IF NOT EXISTS section;
CREATE TABLE IF NOT EXISTS section.section (
  section_id int NOT NULL,
  class_id int NOT NULL, 
  course_id int NOT NULL,
  course_name VARCHAR (255),
  section_desc VARCHAR (255),
  materials VARCHAR (255),
  CONSTRAINT PK_section PRIMARY KEY (section_id, class_id, course_id)
);

CREATE TABLE IF NOT EXISTS section.quiz (
  quiz_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  section_id int,
  class_id int,
  course_id int,
  total_mark int, 
  quiz_type VARCHAR (255),
  FOREIGN KEY (section_id, class_id, course_id) REFERENCES section(section_id, class_id, course_id)
);

CREATE TABLE IF NOT EXISTS section.question (
  qn_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  quiz_id int NOT NULL,
  quiz_desc VARCHAR (255),
  quiz_ans VARCHAR (255),
  question_option VARCHAR (255),
  mark int, 
  CONSTRAINT question_fk_quiz FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);



CREATE DATABASE IF NOT EXISTS course;
CREATE TABLE course.course (
  course_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  course_name VARCHAR (255),
  course_desc VARCHAR (255),
  pre_req VARCHAR (255),
  course_active VARCHAR (255)
);

CREATE TABLE IF NOT EXISTS course.class (
  class_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  intake int,
  emp_id int NOT NULL, 
  emp_name VARCHAR (255),
  course_id int NOT NULL,
  seat_left int, 
  start_date date, 
  end_date date,
  start_enrol date, 
  end_enrol date,
  CONSTRAINT FK_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE IF NOT EXISTS course.class_list (
  emp_id int,
  emp_name VARCHAR (255),
  class_id int NOT NULL,
  progress VARCHAR (255),
  class_status VARCHAR (255),
  ungraded_result VARCHAR (255),
  graded_result VARCHAR (255),
  CONSTRAINT PK_learner PRIMARY KEY (emp_id, class_id),
  CONSTRAINT learner_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE IF NOT EXISTS course.pending_enrolment (
  emp_id int NOT NULL,
  emp_name VARCHAR (255),
  course_id int NOT NULL,
  class_id int NOT NULL,
  pending_status VARCHAR (255),
  CONSTRAINT pk_pending PRIMARY KEY (emp_id, class_id, course_id),
  CONSTRAINT pending_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT pending_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);


CREATE DATABASE IF NOT EXISTS employee;

CREATE TABLE IF NOT EXISTS employee.employee (
  emp_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  emp_name VARCHAR (255) NOT NULL,
  emp_password VARCHAR (255),
  email VARCHAR (255),
  phone int(8),
  dept VARCHAR (255)
);

CREATE TABLE IF NOT EXISTS employee.learner (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255),
  courses_ongoing VARCHAR (255),
  courses_completed VARCHAR (255),
  courses_incompleted VARCHAR (255),
  badge VARCHAR (255),
  CONSTRAINT learner_id FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

CREATE TABLE IF NOT EXISTS employee.trainer (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255),
  courses_teaching VARCHAR (255),
  courses_completed VARCHAR (255),
  CONSTRAINT trainer_id FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

DROP DATABASE IF EXISTS learningsystem;