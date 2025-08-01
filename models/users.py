from database import db
from flask_login import UserMixin 

class User(UserMixin, db.Model):
  #id, username, password, email, role
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True)
  role = db.Column(db.String(20), nullable=False, default='user')