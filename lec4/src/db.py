from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
  """
  Task Model
  """
  __tablename__ = "task"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String, nullable=False)
  done = db.Column(db.Boolean, nullable=False)

  def __init__(self, **kwargs):
    """
    Initialize a Task Object
    """
    self.description = kwargs.get("description", "")
    self.done = kwargs.get("done", False)

  def serialize(self):
    """
    Serialize a Task object into a dictionary
    """
    return {
      "id": self.id,
      "description": self.description,
      "done": self.done
    }

class Subtask(db.Model):
  """
  Subtask Model
  """
  __tablename__ = "subtask"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String, nonlocalble=False)
  done = db.Column(db.Boolean, nullable=False)
  task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

  def __init__(self, **kwargs):
    """
    Initialize a Subtask Object
    """
    self.description = kwargs.get("description", "")
    self.done = kwargs.get("done", False)
    self.task_id = kwargs.get("task_id")

  def serialize(self):
    return {
      "id": self.id,
      "description": self.description,
      "done": self.done,
      "task_id": self.task_id
    }
# implement database model classes
