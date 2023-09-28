from db import db


class UserRecords(db.Model):
    __tablename__ = "users_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"))
