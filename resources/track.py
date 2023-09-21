import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import tracks


blp = Blueprint("Tracks", "tracks", description="Operations on tracks")


@blp.route("/track/<string:track_id>")
class Track(MethodView):
    def get(self, track_id):
        pass

    def delete(self, track_id):
        pass

    def put(self, track_id):
        pass

class TrackList(MethodView):
    def get(self):
        pass

    def post(self):
        pass
