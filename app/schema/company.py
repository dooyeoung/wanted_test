from marshmallow import Schema, fields


class CompanySchema(Schema):
    uuid = fields.UUID(required=True)
    created_at = fields.Str(required=True)
