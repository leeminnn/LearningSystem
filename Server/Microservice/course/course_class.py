def to_json(self):
    return {
        "course_id" : self.course_id,
        "course_name" : self.course_name,
        "course_desc" : self.course_desc,
        "pre-requisite" : self.pre_requisite
    }

class Course (db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key = True)
    