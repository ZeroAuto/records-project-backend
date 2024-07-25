from db import db
from sqlalchemy.sql import false
from sqlalchemy.schema import UniqueConstraint

class UserRecordModel(db.Model):
    __tablename__ = "users_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"))
    notes = db.Column(db.String(255))
    purchased = db.Column(db.Boolean, server_default=false())

    __table_args__ = (
        UniqueConstraint('user_id', 'record_id', name='unique_user_record'),
    )
