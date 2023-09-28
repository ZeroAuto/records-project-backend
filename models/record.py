from db import db

class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artists.id"),
        unique=False,
        nullable=False
    )
    artist = db.relationship("ArtistModel", back_populates="records")
    tracks = db.relationship(
        "TrackModel",
        back_populates="record",
        lazy="dynamic",
        cascade="all, delete",
    )
    users = db.relationship("UserModel", back_populates="records", secondary="users_records")
    description = db.Column(db.String(255))
