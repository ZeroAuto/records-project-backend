from db import db

class TrackModel(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.Integer, nullable=False, unique=False)
    length = db.Column(db.Float(precision=2), unique=False, nullable=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"), unique=False, nullable=False)
    record = db.relationship("RecordModel", back_populates="tracks")
