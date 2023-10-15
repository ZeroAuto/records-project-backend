from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import (
    ArtistModel,
    RecordModel,
)
from schemas import (
    RecordDumpSchema,
    RecordUpdateSchema,
)


def find_or_create_artist(artist_name):
    artist = ArtistModel.query.filter(
        ArtistModel.name == artist_name
    ).first()
    # if the artist doesn't exist create it
    if artist is None:
        artist = ArtistModel(name=artist_name)
        db.session.add(artist)
        db.session.commit()

    return artist


blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordDumpSchema)
    def get(cls, record_id):
        record = RecordModel.query.get_or_404(record_id)
        return record

    def delete(cls, record_id):
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": "Record deleted"}, 200

    @blp.arguments(RecordUpdateSchema)
    @blp.response(200, RecordDumpSchema)
    def put(cls, record_data, record_id):
        record = RecordModel.query.get(record_id)

        if record:
            if "artist" in record_data:
                artist = find_or_create_artist(record_data['artist'])
                record.artist_id = artist.id
            record.name = record_data["name"]
            record.year = record_data["year"]
            record.format = record_data["format"]
        try:
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="An IntegrityError error occurred",
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred during record creation"
            )

        return record


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, RecordDumpSchema(many=True))
    def get(cls):
        records = db.session.query(
            RecordModel.id,
            RecordModel.name,
            RecordModel.year,
            RecordModel.format,
            ArtistModel.name.label('artist_name'),
        ).join(
            ArtistModel,
            ArtistModel.id == RecordModel.artist_id
        )

        return records

    @jwt_required()
    @blp.arguments(RecordUpdateSchema)
    @blp.response(201, RecordDumpSchema)
    def post(cls, record_data):
        artist = find_or_create_artist(record_data["artist"])
        artist_id = artist.id
        record = RecordModel(
            name=record_data["name"],
            artist_id=artist_id,
            year=record_data["year"],
            format=record_data["format"]
        )
        try:
            db.session.add(record)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="An IntegrityError error occurred",
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred during record creation"
            )

        return record
