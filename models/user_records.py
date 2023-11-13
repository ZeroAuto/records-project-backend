from db import db


class UserRecordModel(db.Model):
    __tablename__ = "users_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"))
    notes = db.Column(db.String(255))
