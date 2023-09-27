from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import RecordModel
from schemas import RecordSchema


blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
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
    @blp.response(200, RecordSchema(many=True))
    def get(cls):
        return RecordModel.query.all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(cls, record_data):
        record = RecordModel(**record_data)
        try:
            db.session.add(record)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A record with that name already exists",
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred during record creation"
            )

        return record
