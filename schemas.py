from marshmallow import Schema, fields, validates, ValidationError
from email_validator import validate_email, EmailNotValidError


class ArtistSchema(Schema):
    name = fields.Str(dump_only=True)
    bio = fields.Str(dump_only=True)


class PlainRecordSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    year = fields.Int()
    format = fields.Str()
    artist_id = fields.Int()
    album_art_url = fields.Str()


class RecordUpdateSchema(PlainRecordSchema):
    artist = fields.Str()
    purchased = fields.Boolean(missing=False)


class RecordDumpSchema(PlainRecordSchema):
    artist_name = fields.Str(dump_only=True)


class RecordFindDumpSchema(RecordDumpSchema):
    owned_by_user = fields.Boolean(dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class LoginSchema(PlainUserSchema):
    password = fields.Str(required=True)


class UserSchema(LoginSchema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)

    @validates("email")
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError(str(e))


class RecordFindSchema(Schema):
    name = fields.Str(required=True)
    artist = fields.Str(required=True)


class SearchTextSchema(Schema):
    searchTerm = fields.Str()
    sortColumn = fields.Str()
    sortDirection = fields.Str()
    purchased = fields.Boolean(missing=None)
    offset = fields.Int()
    limit = fields.Int(missing=20)


class DeleteUserRecordSchema(Schema):
    record_id = fields.Int(required=True)


class PostUserRecordSchema(Schema):
    record_id = fields.Int(required=True)
    purchased = fields.Boolean(missing=False)


class UpdateUserRecordSchema(PostUserRecordSchema):
    user_id = fields.Int(required=True)


class UserRecordDumpSchema(Schema):
    record_id = fields.Int(dump_only=True)
    purchased = fields.Boolean(dump_only=True)
    user_id = fields.Int(dump_only=True)
    id = fields.Int(dump_only=True)
