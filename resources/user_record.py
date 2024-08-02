from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
# from sqlalchemy import text
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import UserRecordModel
from schemas import AddUserRecordSchema, UserRecordDumpSchema


blp = Blueprint("UserRecords", "user_records", description="Operations on users_records")


@blp.route("/user_record/add")
class AddRecord(MethodView):
    @jwt_required()
    @blp.arguments(AddUserRecordSchema)
    @blp.response(200, UserRecordDumpSchema)
    def post(cls, data):
        user_id = get_jwt_identity()
        user_record = UserRecordModel(
            record_id=data["record_id"],
            user_id=user_id,
            purchased=data['purchased']
        )
        db.session.add(user_record)
        db.session.commit()

        return user_record
