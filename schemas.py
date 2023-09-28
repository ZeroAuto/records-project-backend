from marshmallow import Schema, fields

class PlainTrackSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    position = fields.Int(required=True)
    length = fields.Float(required=True)

class PlainRecordSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    artist = fields.Str(required=True)

class UserRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    record_id = fields.Int(required=True)

class TrackUpdateSchema(Schema):
    name = fields.Str()
    position = fields.Int()
    length = fields.Float()

class RecordUpdateSchema(Schema):
    name = fields.Str()
    artist = fields.Str()

class TrackSchema(PlainTrackSchema):
    record_id = fields.Int(required=True, load_only=True)
    record = fields.Nested(PlainRecordSchema(), dump_only=True)

class RecordSchema(PlainRecordSchema):
    tracks = fields.List(fields.Nested(PlainTrackSchema()), dump_only=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

class LoginSchema(PlainUserSchema):
    password = fields.Str(required=True)

class UserSchema(PlainUserSchema):
    email = fields.Int(required=True)
    name = fields.Int(required=True)
