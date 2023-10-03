from db import db


class ArtistModel(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    records = db.relationship(
        "RecordModel",
        back_populates="artist",
        lazy="dynamic",
        cascade="all, delete",
    )
    bio = db.Column(db.String)
