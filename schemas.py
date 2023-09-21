from marshmallow import Schema, fields


class TrackSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    position = fields.Int(required=True)
    length = fields.Float(required=True)
    record_id = fields.Str(required=True)


class TrackUpdateSchema(Schema):
    name = fields.Str()
    position = fields.Int()
    length = fields.Float()


class RecordSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    artist = fields.Str(required=True)
