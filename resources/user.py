from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError

from db import db
from models import UserModel, UserRecordModel
from schemas import (
    LoginSchema,
    UserSchema,
)
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "name": user.name,
                "id": user.id,
                "admin": user.admin,
            }, 200

        abort(401, message="Invalid credentials")


@blp.route("/signup")
class UserSignup(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email address already exists.")

        user = UserModel(
            name=user_data["name"],
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        try:
            db.session.add(user)
            db.session.flush()
            db.session.refresh(user)
            db.session.commit()

        except ValidationError:
            abort(
                409,
                message="A Validation error occurred",
            )

        except IntegrityError:
            abort(
                400,
                message="An IntegrityError error occurred",
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred during user creation"
            )
        finally:
            if user:
                access_token = create_access_token(
                    identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "name": user.name,
                    "id": user.id,
                    "admin": user.admin,
                }, 200

        return {"message": "User"}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
#
#
# @blp.route("/user/<int:user_id>")
# class User(MethodView):
#     """
#     This resource can be useful when testing our Flask app.
#     We may not want to expose it to public users, but for the
#     sake of demonstration in this course, it can be useful
#     when we are manipulating data regarding the users.
#     """
#
#     @blp.response(200, UserSchema)
#     def get(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         return user
#
#     def delete(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return {"message": "User deleted."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.query.filter(
            UserModel.id == user_id,
        ).first()
        new_token = create_access_token(identity=user.id, fresh=False)
        new_refresh_token = create_refresh_token(user.id)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {
            "access_token": new_token,
            "refresh_token": new_refresh_token,
            "name": user.name,
            "id": user.id,
        }, 200
