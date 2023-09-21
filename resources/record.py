import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import records
from schemas import RecordSchema


blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(cls, record_id):
        try:
            # You presumably would want to include the record's items here too
            # More on that when we look at databases
            return records[record_id]
        except KeyError:
            abort(404, message="Record not found.")

    def delete(cls, record_id):
        try:
            del records[record_id]
            return {"message": "Record deleted."}
        except KeyError:
            abort(404, message="Record not found.")


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, RecordSchema(many=True))
    def get(cls):
        return records.values()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(cls, record_data):
        for record in records.values():
            if record_data["name"] == record["name"]:
                abort(400, message=f"Record already exists.")

        record_id = uuid.uuid4().hex
        record = {**record_data, "id": record_id}
        records[record_id] = record

        return record
