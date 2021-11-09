CREATE DATABASE IF NOT EXISTS section;
CREATE TABLE IF NOT EXISTS section.section (
  section_id int NOT NULL,
  class_id int NOT NULL, 
  course_id int NOT NULL,
  materials VARCHAR (255),
  CONSTRAINT PK_section PRIMARY KEY (section_id, class_id, course_id)
);
INSERT INTO section.section (section_id, class_id, course_id, materials) 
VALUES ('1', '1', '1', ' ');

CREATE TABLE IF NOT EXISTS section.quiz (
  quiz_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  section_id int,
  class_id int,
  course_id int,
  total_mark int DEFAULT '0', 
  quiz_time int,
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
  pre_req VARCHAR (255) DEFAULT 'No Prerequisite Course',
  course_active VARCHAR (255) DEFAULT 'active'
);
ALTER TABLE course.course AUTO_INCREMENT=100;

CREATE TABLE IF NOT EXISTS course.class (
  class_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  intake int,
  emp_id int NOT NULL, 
  emp_name VARCHAR (255),
  course_id int NOT NULL,
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
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('1', 'Amy Tan', '1234', 'amy_tan@gmail.com', '81234567', 'Electronic & Controls');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('2', 'Joy Lim', '1234', 'joylim@gmail.com', '82345678', 'Electrical Service');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('3', 'Cassy Toh', '1234', 'cassy_toh@gmail.com', '83456789', 'Mechanical Service');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('4', 'Paul Kor', '1234', 'paulkor@gmail.com', '84567890', 'Electronic & Controls');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('5', 'Jack Lim', '1234', 'Jacklim@gmail.com', '85678912', 'Mechanical Service');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('6', 'Peter Ong', '1234', 'Peter_ong@gmail.com', '91234567', 'Electronic & Controls');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('7', 'Lyn Tan', '1234', 'Lyn_tan@gmail.com', '92345678', 'Mechanical Service');
INSERT INTO employee.employee (emp_id, emp_name, emp_password, email, phone, dept) 
VALUES ('8', 'Joel Lim', '1234', 'Joellim@gmail.com', '93456789', 'Electrical Service');

CREATE TABLE IF NOT EXISTS employee.learner (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255),
  courses_ongoing VARCHAR (255) DEFAULT ',' ,
  courses_completed VARCHAR (255)  DEFAULT ',' , 
  courses_incompleted VARCHAR (255) DEFAULT ',' ,
  badge VARCHAR (255),
  CONSTRAINT learner_id FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

INSERT INTO employee.learner (emp_id, emp_name) 
VALUES ('1','Amy Tan');
INSERT INTO employee.learner (emp_id, emp_name) 
VALUES ('2','Joy Lim');
INSERT INTO employee.learner (emp_id, emp_name) 
VALUES ('3','Cassy Toh');
INSERT INTO employee.learner (emp_id, emp_name) 
VALUES ('4','Paul Kor');

CREATE TABLE IF NOT EXISTS employee.trainer (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255),
  courses_teaching VARCHAR (255) DEFAULT ',' ,
  courses_completed VARCHAR (255) DEFAULT ',' ,
  CONSTRAINT trainer_id FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

INSERT INTO employee.trainer (emp_id, emp_name) 
VALUES ('5','Jack Lim');
INSERT INTO employee.trainer (emp_id, emp_name) 
VALUES ('6','Peter Ong');
INSERT INTO employee.trainer (emp_id, emp_name) 
VALUES ('7','Lyn Tan');
INSERT INTO employee.trainer (emp_id, emp_name) 
VALUES ('8','Joel Lim');

DROP DATABASE IF EXISTS learningsystem;