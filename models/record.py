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
    users = db.relationship(
        "UserModel", back_populates="records", secondary="users_records")
    description = db.Column(db.String(255))
    year = db.Column(db.Integer)
    format = db.Column(db.String)
    album_art_url = db.Column(db.String)
    db.UniqueConstraint(name, artist_id)
