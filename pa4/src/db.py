from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here
association_table = db.Table(
    "association",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
)


class Course(db.Model):
    """
    Course Model
    """

    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    students = db.relationship(
        "User", secondary=association_table, back_populates="courses"
    )
    instructors = db.relationship(
        "User", secondary=association_table, back_populates="courses"
    )

    def __init__(self, **kwargs):
        """
        Initializes a new Course object.
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serializes a Course object into a dictionary.
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [s.serialize() for s in self.assignments],
            "instructors": [u.serialize() for u in self.instructors],
            "students": [u.serialize() for u in self.students],
        }

    def simple_serialize(self):
        """
        Serializes course object into a dictionary with only id, code and name.
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }


class Assignment(db.Model):
    """
    Assignment Model
    """

    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Interval, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes a new Assignment object.
        """
        self.title = kwargs.get("title", "")
        self.duedate = kwargs.get("duedate", "")

    def serialize(self):
        """
        Serializes a Assignment object into a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "duedate": self.duedate,
            "course": [c.simple_serialize() for c in self.courses],
        }


class User(db.Model):
    """
    User Model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    netid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    courses = db.relationship(
        "Course", secondary=association_table, back_populates="instructors"
    )
    courses1 = db.relationship(
        "Course", secondary=association_table, back_populates="students"
    )

    def __init__(self, **kwargs):
        """
        Initializes a User Object
        """
        self.netid = kwargs.get("netid", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serializes a User Object into a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in self.courses]
            + [d.simple_serialize() for d in self.courses1],
        }
