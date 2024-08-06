from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from db import db
from models import ArtistModel

from schemas import ArtistDumpSchema, ArtistSearchSchema


blp = Blueprint("Artists", "artists", description="Operations on artists")


@blp.route("/artist/find")
class FindArtistByName(MethodView):
    # @jwt_required()
    @blp.arguments(ArtistSearchSchema, location="query")
    @blp.response(200, ArtistDumpSchema(many=True))
    def get(cls, data):
        search_term = data["search_term"]
        artists = ArtistModel.query.filter(
            ArtistModel.name.ilike(f'%{search_term}%')
        ).all()

        return artists
