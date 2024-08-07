from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import RecordModel, UserRecordModel
from schemas import (
    PostUserRecordSchema,
    UpdateUserRecordSchema,
    UserRecordDumpSchema
)


blp = Blueprint("UserRecords", "user_records", description="Operations on users_records")


@blp.route("/user_record")
class AddRecord(MethodView):
    @jwt_required()
    @blp.arguments(PostUserRecordSchema)
    @blp.response(200, UserRecordDumpSchema)
    def post(cls, data):
        user_id = get_jwt_identity()
        user_record = UserRecordModel(
            record_id=data["record_id"],
            user_id=user_id,
            purchased=data['purchased']
        )
        db.session.add(user_record)

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
                message="An error occurred during user_record creation"
            )

        return user_record


@blp.route("/user_record/<string:user_record_id>")
class UserRecord(MethodView):
    @jwt_required()
    @blp.response(200, UserRecordDumpSchema)
    def delete(cls, user_record_id):
        user_record = UserRecordModel.query.get_or_404(user_record_id)
        db.session.delete(user_record)
        db.session.commit()
        return user_record

    @jwt_required()
    @blp.arguments(UpdateUserRecordSchema)
    @blp.response(200, UserRecordDumpSchema)
    def put(cls, data, user_record_id):
        user_record = UserRecordModel.query.get_or_404(user_record_id)
        user_record.purchased = data["purchased"]
        user_record.record_id = data["record_id"]
        user_record.user_id = data["user_id"]

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
                message="An error occurred during user_record update"
            )

        return user_record
