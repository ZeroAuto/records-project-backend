from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from db import db
from models import UserRecordModel
from schemas import (
    AddUserRecordSchema,
    DeleteUserRecordSchema,
    UserRecordDumpSchema
)


blp = Blueprint("UserRecords", "user_records", description="Operations on users_records")


@blp.route("/user_record")
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

@blp.route("/user_record/<string:user_record_id>")
class UserRecord(MethodView):
    @jwt_required()
    @blp.response(200, UserRecordDumpSchema)
    def delete(cls, user_record_id):
        user_record = UserRecordModel.query.get_or_404(user_record_id)
        db.session.delete(user_record)
        db.session.commit()
        return user_record
