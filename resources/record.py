from flask.views import MethodView
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


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, RecordDumpSchema(many=True))
    def get(cls):
        return RecordModel.query.all()

    @blp.arguments(RecordUpdateSchema)
    @blp.response(201, RecordDumpSchema)
    def post(cls, record_data):
        artist = ArtistModel.query.filter(
            ArtistModel.name == record_data["artist"]
        ).first()
        # if the artist doesn't exist create it
        if artist is None:
            artist = ArtistModel(name=record_data["artist"])
            db.session.add(artist)
            db.session.commit()
            print(artist.id, flush=True)
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
        except IntegrityError as e:
            abort(
                400,
                # message="An IntegrityError error occurred",
                message=e.args,
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred during record creation"
            )

        return record
