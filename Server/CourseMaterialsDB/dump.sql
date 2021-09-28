CREATE TABLE Employee (
  emp_id int NOT NULL PRIMARY KEY,
  emp_name VARCHAR (255) NOT NULL,
  email VARCHAR (255) NOT NULL,
  phone int(8) NOT NULL,
  position VARCHAR (255) NOT NULL,
  dept VARCHAR (255) NOT NULL,
  course_complete VARCHAR (255) NOT NULL,
  badge VARCHAR (255) NOT NULL
);

CREATE TABLE course (
  course_id int NOT NULL PRIMARY KEY,
  course_name VARCHAR (255) NOT NULL,
  start_date date NOT NULL, 
  end_date date NOT NULL,
  pre_req VARCHAR (255) NOT NULL
);

CREATE TABLE class (
  class_id int NOT NULL PRIMARY KEY,
  class_name VARCHAR (255) NOT NULL,
  intake VARCHAR (255) NOT NULL,
  emp_id int, 
  course_id int,
  CONSTRAINT FK_emp_id FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT FK_course_id FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE learner_list (
  emp_id int, 
  class_id int,
  progress VARCHAR (255) NOT NULL,
  status VARCHAR (255) NOT NULL,
  CONSTRAINT PK_learner PRIMARY KEY (emp_id, class_id),
  CONSTRAINT learner_fk_emp FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT learner_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE pending_enrolment (
  emp_id int,
  course_id int,
  class_id int,
  status VARCHAR (255) NOT NULL,
  CONSTRAINT pk_pending PRIMARY KEY (emp_id, class_id, course_id),
  CONSTRAINT pending_fk_emp FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT pending_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT pending_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE forum (
  forum_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  emp_id int, 
  class_id int,
  course_id int,
  role VARCHAR (255) NOT NULL,
  message VARCHAR (255) NOT NULL,
  forum_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT forum_fk_emp FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT forum_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT forum_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE section (
  section_id int NOT NULL PRIMARY KEY,
  section_name VARCHAR (255) NOT NULL,
  section_desc VARCHAR (255) NOT NULL,
  class_id int, 
  course_id int,
  materials VARCHAR (255) NOT NULL,
  CONSTRAINT section_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT section_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE quiz (
  quiz_id int NOT NULL PRIMARY KEY,
  section_id int,
  class_id int,
  course_id int,
  total_mark int NOT NULL, 
  CONSTRAINT quiz_fk_section FOREIGN KEY (section_id) REFERENCES section(section_id),
  CONSTRAINT quiz_fk_class FOREIGN KEY (class_id) REFERENCES class(class_id),
  CONSTRAINT quiz_fk_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE question (
  qn_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  quiz_id int,
  quiz_desc VARCHAR (255) NOT NULL,
  quiz_ans VARCHAR (255) NOT NULL,
  mark int NOT NULL, 
  CONSTRAINT question_fk_quiz FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
)