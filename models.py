from flask_login import UserMixin
from datetime import datetime
from db_config import *



class FileContens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    create = db.Column(db.DateTime, default=datetime.utcnow)
    bites = db.Column(db.Float)
    sha = db.Column(db.String(300))



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
       