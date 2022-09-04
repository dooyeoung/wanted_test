from marshmallow import Schema, fields


class CompanySchema(Schema):
    class Meta:
        ordered = False

    company_name = fields.Str(
        required=True,
        metadata={
            "description": "회사명",
            "example": "라인프레쉬",
        },
    )
    tags = fields.List(
        fields.Str,
        required=True,
        metadata={
            "description": "태그 목록",
            "example": ["태그_1", "태그_8", "태그_15"],
        },
    )


class NewCompanySchema(Schema):
    class Meta:
        ordered = False

    company_name = fields.Dict(
        keys=fields.Str(),
        values=fields.Str(),
        required=True,
        metadata={
            "description": "여러 언어의 회사명",
            "example": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
        },
    )
    tags = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Dict()),
        required=True,
        metadata={
            "description": "여러 언어의 태그",
            "exmaple": [
                {
                    "tag_name": {
                        "ko": "태그_1",
                        "tw": "tag_1",
                        "en": "tag_1",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_8",
                        "tw": "tag_8",
                        "en": "tag_8",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_15",
                        "tw": "tag_15",
                        "en": "tag_15",
                    }
                },
            ],
        },
    )


class CompanyNameSchema(Schema):
    company_name = fields.Str(
        required=True, metadata={"description": "회사명", "exmaple": "라인프레쉬"}
    )


class CompanyQueryArgsSchema(Schema):
    query = fields.Str(
        required=True, metadata={"description": "회사명 또는 태그", "exmaple": "`라인`, `태그_1`"}
    )


class NewTagSchema(Schema):
    tag_name = fields.Dict(
        keys=fields.Str(),
        values=fields.Str(),
        required=True,
        metadata={
            "description": "추가할 태그",
            "exmaple": {
                "ko": "태그_4",
                "tw": "tag_4",
                "en": "tag_4",
            },
        },
    )


class CompanyTagDeleteSchema(Schema):
    class Meta:
        ordered = False

    company_name = fields.Str(
        required=True, metadata={"description": "회사명", "exmaple": "라인프레쉬"}
    )
    tag_name = fields.Str(
        required=True, metadata={"description": "삭제할 태그", "exmaple": "태그_1"}
    )
