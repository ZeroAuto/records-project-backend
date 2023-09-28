from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import UserRecords
from schemas import UserRecordSchema

@blp.route("/user/login")
class UserLogin(MethodView):
    # do things


@blp.route("/user/signup"):
class UserSignup(MethodView):
    # @blp.arguments(UserSignupSchema)
    # @blp.response(201, UserSchema)
    def post(self, user_data):
        # do somet things


@blp.route("/user/add_record"):
class LinkUserToRecord(MethodView):
    @blp.arguments(UserRecordSchema)
    @blp.response(201, UserRecordSchema)
    def post(self, user_id, record_id):
        if UserRecords.query.filter(UserRecords.record_id == record_id, UserRecords.user_id == user_id):
            abort(400, message="User has already added this record")

        user_record = UserRecords(user_id = user_id, record_id = record_id)

        try:
            db.session.add(user_record)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return user_record
