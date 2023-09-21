import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import tracks
from schemas import TrackSchema, TrackUpdateSchema


blp = Blueprint("Tracks", "tracks", description="Operations on tracks")


@blp.route("/track/<string:track_id>")
class Track(MethodView):
    @blp.response(200, TrackSchema)
    def get(self, track_id):
        try:
            return tracks[track_id]
        except KeyError:
            abort(404, message="Track not found.")

    def delete(self, track_id):
        try:
            del tracks[track_id]
            return {"message": "Track deleted."}
        except KeyError:
            abort(404, message="Track not found.")

    @blp.arguments(TrackUpdateSchema)
    @blp.response(200, TrackSchema)
    def put(self, track_data, track_id):
        try:
            track = tracks[track_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            track |= track_data

            return track
        except KeyError:
            abort(404, message="Track not found.")


@blp.route("/track")
class TrackList(MethodView):
    @blp.response(200, TrackSchema(many=True))
    def get(self):
        return tracks.values()

    @blp.arguments(TrackSchema)
    @blp.response(201, TrackSchema)
    def post(self, track_data):
        for track in tracks.values():
            if (
                track_data["name"] == track["name"]
                and track_data["store_id"] == track["store_id"]
            ):
                abort(400, message=f"Track already exists.")

        track_id = uuid.uuid4().hex
        track = {**track_data, "id": track_id}
        tracks[track_id] = track

        return track
