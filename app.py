import os
import secrets

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from db import db

from resources.record import blp as RecordBluePrint
from resources.user import blp as UserBluePrint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Records REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(
        app,
        origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    )
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    # app.config["JWT_SECRET_KEY"] = "mikej"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(RecordBluePrint)
    api.register_blueprint(UserBluePrint)

    return app
