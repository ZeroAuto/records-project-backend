import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TrackModel
from schemas import TrackSchema, TrackUpdateSchema


blp = Blueprint("Tracks", "tracks", description="Operations on tracks")


@blp.route("/track/<string:track_id>")
class Track(MethodView):
    @blp.response(200, TrackSchema)
    def get(self, track_id):
        track = TrackModel.query.get_or_404(track_id)

    def delete(self, track_id):
        track = TrackModel.query.get_or_404(track_id)
        db.session.delete(track)
        db.session.commit()
        return {"message": "Track deleted"}

    @blp.arguments(TrackUpdateSchema)
    @blp.response(200, TrackSchema)
    def put(self, track_data, track_id):
        track = TrackModel.query.get(track_id)

        if track:
            track.position = track_data["position"]
            track.length = track_data["length"]
            track.name = track_data["name"]
        else:
            track = TrackModel(id=track_id, **track_data)

        db.session.add(track)
        db.session.commit()

        return track


@blp.route("/track")
class TrackList(MethodView):
    @blp.response(200, TrackSchema(many=True))
    def get(self):
        return TrackModel.query.all()

    @blp.arguments(TrackSchema)
    @blp.response(201, TrackSchema)
    def post(self, track_data):
        track = TrackModel(**track_data)

        try:
            db.session.add(track)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occured during track creation"
            )

        return track
