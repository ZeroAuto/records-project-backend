from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy import text
# from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import (
    ArtistModel,
    RecordModel,
    UserRecordModel,
)
from schemas import (
    RecordDumpSchema,
    RecordFindSchema,
    RecordUpdateSchema,
    SearchTextSchema,
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


def record_query(search_text="", user_id=None, purchased=None):
    select_sql = "SELECT r.id, r.name, r.year, r.format, a.name as artist_name"
    from_sql = "FROM records as r"
    join_terms = ["JOIN artists as a on r.artist_id = a.id"]
    params = {}
    where_terms = []

    if len(search_text) > 0:
        search_term = f"%{search_text}%"
        params["search_text"] = search_term
        where_sql = "(r.name ilike :search_text or a.name ilike :search_text)"
        where_terms.append(where_sql)

    if user_id:
        join_terms.append("JOIN users_records as ur on r.id = ur.record_id")
        join_terms.append("JOIN users as u on ur.user_id = u.id")
        params["user_id"] = int(user_id)
        where_terms.append("u.id = :user_id")

        if purchased is not None:
            params["purchased"] = purchased
            where_terms.append("ur.purchased = :purchased")

    query = select_sql + " " + from_sql + " " + " ".join(join_terms)

    if len(search_text) > 0 or user_id:
        query = query + " WHERE " + " AND ".join(where_terms)

    records = db.session.execute(text(query), params)
    return records


blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/add/<string:record_id>")
class AddRecord(MethodView):
    @jwt_required()
    @blp.response(200, RecordDumpSchema)
    def post(cls, record_id):
        user_id = get_jwt_identity()
        user_record = UserRecordModel(
            record_id=record_id,
            user_id=user_id,
        )
        db.session.add(user_record)
        db.session.commit()


@blp.route("/record/find")
class FindRecordByNameAndArtist(MethodView):
    @blp.arguments(RecordFindSchema, location="query")
    @blp.response(200, RecordDumpSchema)
    def get(cls, record_data):
        record = db.session.query(
            RecordModel.id,
            RecordModel.name,
            RecordModel.year,
            RecordModel.format,
            ArtistModel.name,
        ).join(
            ArtistModel,
            ArtistModel.id == RecordModel.artist_id
        ).filter(
            RecordModel.name == record_data["name"],
            ArtistModel.name == record_data["artist"]
        ).first()

        return record


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


@blp.route("/record/user")
class UserRecord(MethodView):
    @jwt_required()
    @blp.arguments(SearchTextSchema, location="query")
    @blp.response(200, RecordDumpSchema(many=True))
    def get(cls, data):
        user_id = get_jwt_identity()
        query = record_query(
            search_text=data["text"],
            user_id=user_id,
        )

        return query


@blp.route("/record")
class RecordList(MethodView):
    @blp.arguments(SearchTextSchema, location="query")
    @blp.response(200, RecordDumpSchema(many=True))
    def get(cls, data):
        query = record_query(search_text=data["text"])

        return query

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
            db.session.flush()
            db.session.refresh(record)
            user_id = get_jwt_identity()
            user_record = UserRecordModel(
                record_id=record.id,
                user_id=user_id,
            )
            db.session.add(user_record)
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
