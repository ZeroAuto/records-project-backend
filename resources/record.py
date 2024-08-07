from flask import jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload

from db import db
from models import (
    ArtistModel,
    RecordModel,
    UserRecordModel,
)
from schemas import (
    RecordDumpSchema,
    RecordFindSchema,
    RecordFindDumpSchema,
    RecordUpdateSchema,
    SearchTextSchema,
    UpdateUserRecordSchema,
)


def find_or_create_artist(artist_name):
    artist = ArtistModel.query.filter(
        ArtistModel.name == artist_name
    ).first()

    if artist is None:
        artist = ArtistModel(name=artist_name)
        db.session.add(artist)
        db.session.commit()

    return artist


def record_query(
        search_text="",
        user_id=None,
        purchased=None,
        sort_column="name",
        sort_direction="asc",
        limit=20,
        offset=0,
    ):
    select_sql = "SELECT r.*, a.name as artist_name"
    count_sql = "SELECT COUNT(*)"
    from_sql = "FROM records as r"
    join_terms = ["JOIN artists as a on r.artist_id = a.id"]
    params = {}
    where_terms = []

    if len(search_text) > 0:
        search_terms = search_text.split()
        for idx, term in enumerate(search_terms):
            param = f"search_term_{idx}"
            params[param] = f"%{term}%"
            where_terms.append(
                f"""
                    (r.name ilike :{param}
                    or
                    a.name ilike :{param})
                """
            )

    if user_id:
        join_type = "LEFT JOIN"
        select_sql += ", ur.purchased, ur.id as users_records_id, ur.user_id"

        if purchased is not None:
            join_type = "JOIN"
            params["purchased"] = purchased
            where_terms.append("ur.purchased = :purchased")

        join_terms.append(f"{join_type} users_records as ur on r.id = ur.record_id AND ur.user_id = :user_id")
        join_terms.append(f"{join_type} users as u on ur.user_id = u.id")
        params["user_id"] = int(user_id)

    query_base = from_sql + " " + " ".join(join_terms)

    if len(search_text) > 0 or user_id and len(where_terms) > 0:
        query_base += " WHERE " + " AND ".join(where_terms)

    query = select_sql + " " + query_base
    count_query = count_sql + " " + query_base

    sort_columns = {
        "name": "r.name",
        "artist": "a.name",
        "format": "r.format",
        "year": "r.year"
    }

    query += f" ORDER BY {sort_columns[sort_column]} {sort_direction}"
    query += f" LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    records = db.session.execute(text(query), params).fetchall()
    total_count = db.session.execute(text(count_query), params).scalar()

    record_dicts = [dict(row._mapping) for row in records]

    return record_dicts, total_count


blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/find")
class FindRecordByNameAndArtist(MethodView):
    @jwt_required()
    @blp.arguments(RecordFindSchema, location="query")
    @blp.response(200, RecordFindDumpSchema)
    def get(cls, record_data):
        user_id = get_jwt_identity()
        record = db.session.query(
            RecordModel.id,
            RecordModel.name,
            RecordModel.year,
            RecordModel.format,
            ArtistModel.name.label('artist_name'),
        ).join(
            ArtistModel,
            ArtistModel.id == RecordModel.artist_id
        ).filter(
            RecordModel.name == record_data["name"],
            ArtistModel.name == record_data["artist"]
        ).first()

        if record:
            # Check if the record is associated with the current user
            association_exists = db.session.query(
                db.exists().where(
                    UserRecordModel.user_id == user_id,
                    UserRecordModel.record_id == record.id
                )
            ).scalar()

            record_dict = record._asdict()  # Convert SQLAlchemy row object to dictionary
            record_dict['owned_by_user'] = association_exists
            return record_dict

        return record


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, RecordDumpSchema)
    def get(cls, record_id):
        current_user = get_jwt_identity()
        record = db.session.query(
            RecordModel.id,
            RecordModel.name,
            RecordModel.year,
            RecordModel.format,
            RecordModel.album_art_url,
            ArtistModel.name.label('artist_name'),
        ).join(
            ArtistModel,
            ArtistModel.id == RecordModel.artist_id
        ).filter(
            RecordModel.id == record_id
        ).first()

        if current_user:
            # Check if the record is associated with the current user
            association_exists = db.session.query(
                db.exists().where(
                    UserRecordModel.user_id == current_user,
                    UserRecordModel.record_id == record.id
                )
            ).scalar()
            record_dict = record._asdict()  # Convert SQLAlchemy row object to dictionary
            record_dict["owned_by_user"] = association_exists

            if association_exists: 
                user_record = db.session.query(UserRecordModel).filter_by(
                    user_id = current_user,
                    record_id = record.id,
                ).first()

                record_dict["purchased"] = user_record.purchased

            return record_dict

        return record

    def delete(cls, record_id):
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": "Record deleted"}, 200

    @blp.arguments(RecordUpdateSchema)
    @blp.response(200, RecordDumpSchema)
    @jwt_required()
    def put(cls, record_data, record_id):
        record = RecordModel.query.get(record_id)
        current_user = get_jwt_identity()

        if record:
            if "artist" in record_data:
                artist = find_or_create_artist(record_data['artist'])
                record.artist_id = artist.id
            record.name = record_data["name"]
            record.year = record_data["year"]
            record.format = record_data["format"]
            record.album_art_url = record_data["album_art_url"]

            if record_data["purchased"] is not None:
                user_record = db.session.query(UserRecordModel).filter_by(
                    user_id = current_user,
                    record_id = record.id,
                ).first()
                if user_record:
                    user_record.purchased = record_data["purchased"]

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
    @blp.arguments(SearchTextSchema, location="query")
    @blp.response(200, RecordDumpSchema(many=True))
    @jwt_required(optional=True)
    def get(cls, data):
        current_user = get_jwt_identity()
        records, total_count = record_query(
            search_text=data["searchTerm"],
            sort_column=data["sortColumn"],
            sort_direction=data["sortDirection"],
            offset=data["offset"],
            limit=data["limit"],
            user_id=current_user,
            purchased=data["purchased"],
        )

        response = make_response(jsonify(records))
        response.headers["X-Total-Count"] = total_count
        return response

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
            format=record_data["format"],
            album_art_url=record_data["album_art_url"],
        )
        try:
            db.session.add(record)
            db.session.flush()
            db.session.refresh(record)
            user_id = get_jwt_identity()
            user_record = UserRecordModel(
                record_id=record.id,
                user_id=user_id,
                purchased=record_data["purchased"]
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
