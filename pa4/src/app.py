import json

from db import db
from flask import Flask, request
from db import Course
from db import Assignment

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here


@app.route("/api/courses/", methods=["GET"])
def get_courses():
    """
    Endpoint for getting all courses
    """
    courses = [course.serialize() for course in Course.query.all()]
    return success_response({"courses": courses})


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a course
    """
    body = json.loads(request.data)
    new_course = Course(code=body.get("code"), name=body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    """
    Endpoint for getting a course with specified course id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for deleting a course by id

    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found!")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    Endpoint for creating an assignment for a course by course id
    """
    body = json.loads(request.data)
    new_assignment = Assignment(
        title=body.get("title"), due_date=body.get("due_date"), course_id=course_id
    )
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    new_user = User(
        name=body.get("name"),
        netid=body.get("netid"),
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize())


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting a user with specified user id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user(course_id):
    """
    Endpoint for adding a user to a course by course id
    """
    course = Course.query.filter_by(id=course_id).first()

    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")

    user = User.query.filter_by(id=user_id.first())
    if user is None:
        return failure_response("User not found")
    if type == "student":
        course.students.append(user)
    if type == "instructor":
        course.instructors.append(user)
    db.sesson.commit()
    return success_response(course.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
