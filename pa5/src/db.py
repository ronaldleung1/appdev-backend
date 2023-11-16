from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

class Course(db.Model):
    """
    Course Model
    """

    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

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
        }