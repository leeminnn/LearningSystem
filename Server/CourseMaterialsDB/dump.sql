CREATE TABLE Quiz (
  user VARCHAR(255) NOT NULL,
  occupation VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL
)

CREATE TABLE Employee (
  emp_id 
  emp_name 
  email 
  phone
  position 
  dept 
  course_complete 
  badge 
)

CREATE TABLE course (
  course_id 
  course_name 
  start_date
  end_date 
  pre_req
)

CREATE TABLE class (
  class_id
  class_name
  intake 
  course_id 
  emp_id 
)

CREATE TABLE learner_list (
  emp_id
  class_id 
  progress 
  status 
)

CREATE TABLE pending_enrolment (
  emp_id 
  course_id 
  class_int 
  status 
)

CREATE TABLE forum (
  forum_id 
  emp_id 
  class_id 
  course_id 
  role 
  message 
  timestamp
)

CREATE TABLE section (
  section_id 
  section_name 
  section_desc 
  class_id 
  course_id 
  materials 
)

CREATE TABLE quiz (
  quiz_id 
  section_id 
  class_id 
  course_id 
  total_mark 
)

CREATE TABLE question (
  qn_id 
  quiz_id 
  quiz_desc 
  quiz_ans 
  mark 
)