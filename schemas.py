from marshmallow import Schema, fields


class ArtistSchema(Schema):
    name = fields.Str(dump_only=True)
    bio = fields.Str(dump_only=True)


class PlainRecordSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    year = fields.Int()
    format = fields.Str()


class UserRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    record_id = fields.Int(required=True)


class TrackUpdateSchema(Schema):
    name = fields.Str()
    position = fields.Int()
    length = fields.Float()


class RecordUpdateSchema(PlainRecordSchema):
    artist = fields.Str()


class RecordDumpSchema(PlainRecordSchema):
    artist = fields.Nested(ArtistSchema(), dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class LoginSchema(PlainUserSchema):
    password = fields.Str(required=True)


class UserSchema(LoginSchema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)
