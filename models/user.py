from db import db
from sqlalchemy.sql import false


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, server_default=false(), nullable=False)
    records = db.relationship(
        "RecordModel", back_populates="users", secondary="users_records")
