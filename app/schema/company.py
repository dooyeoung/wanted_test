from marshmallow import Schema, fields


class CompanySchema(Schema):
    company_name = fields.Str(required=True)
    tags = fields.List(fields.Str, required=True)


class NewCompanySchema(Schema):
    company_name = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True)
    tags = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Dict()), required=True
    )
