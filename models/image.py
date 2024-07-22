from db import db

class ImageModel(db.Model):
    __tablename__ == "images"

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(
        db.Integer,
        db.ForeignKey("records.id"),
        unique=False,
        nullable=False
    )
    record = db.relationship("RecordModel", back_populates="images")
    src_url = db.Column(db.String(255))
    delete_url = db.Column(db.String(255))
