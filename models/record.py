from db import db

class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)
    tracks = db.relationship("TrackModel", back_populates="record", lazy="dynamic")
