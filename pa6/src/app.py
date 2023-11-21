import json

from db import db
from flask import Flask, request
from db import Course
import os

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
@app.route("/")
def get_netid():
    """
    Endpoint for getting NetID environment variable
    """
    return f"{os.environ['NETID']} was here!"

@app.route("/api/courses/", methods=["GET"])
def get_courses():
    """
    Endpoint for getting all courses
    """
    courses = [course.serialize() for course in Course.query.all()]
    return json.dumps({"courses": courses}), 200

@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a course
    """
    body = json.loads(request.data)
    new_course = Course(code=body.get("code"), name=body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return json.dumps(new_course.serialize()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
