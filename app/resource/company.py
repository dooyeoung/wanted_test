from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schema.company import (
    CompanySchema,
    NewCompanySchema,
    NewTagSchema,
    CompanyNameSchema,
    CompanyTagDeleteSchema,
    CompanyQueryArgsSchema,
)
from app.service.dto.company import CompanyNameDTO, CompanyTagDTO
from app.exception import (
    DuplicatedName,
    NotFoundCompany,
    DuplicatedTag,
    NotFoundCompanyTag,
)
from app.components import company_service

api = Blueprint("company", __name__, url_prefix="/")


@api.route("/companies")
class Companies(MethodView):
    @api.arguments(schema=NewCompanySchema)
    @api.response(status_code=200, schema=CompanySchema)
    def post(self, new_company):
        """회사 정보 추가

        한 회사의 각 나라별 이름과 태그 정보를 일괄 등록합니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")
        names = new_company["company_name"]
        tags = new_company["tags"]

        company_names = []
        for language, name in names.items():
            company_names.append(CompanyNameDTO(language=language, name=name))

        company_tags = []
        for tag in tags:
            for language, name in tag["tag_name"].items():
                group_id = int(name.split("_")[-1])
                company_tags.append(
                    CompanyTagDTO(language=language, name=name, group_id=group_id)
                )

        try:
            company_data = company_service().add_commany(
                names=company_names,
                tags=company_tags,
            )
        except DuplicatedName as e:
            exception_data = e.args[0]
            abort(
                400,
                message=f"company name {exception_data.language}-{exception_data.name} is duplicated",  # noqa
            )

        return company_data[response_language]


@api.route("/companies/<string:company_name>")
class CompaniesByname(MethodView):
    @api.arguments(schema=CompanyNameSchema, location="path", as_kwargs=True)
    @api.response(200, CompanySchema)
    def get(self, **path_parameter):
        """회사 정보 조회

        회사명으로 회사정보를 조회합니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")
        company_name = path_parameter["company_name"]
        try:
            company_data = company_service().get_commany_by_name(name=company_name)
        except NotFoundCompany:
            abort(404, message=f"can not found comapny {company_name}")
        return company_data[response_language]

    @api.response(200)
    def delete(self, company_name):
        """회사 정보 삭제

        회사명과 일치하는 정보를 삭제합니다.
        ---
        """
        company_service().delete_company_by_name(name=company_name)
        return {"result": "success"}


@api.route("/search")
class SearchCompanies(MethodView):
    @api.arguments(CompanyQueryArgsSchema, location="query")
    @api.response(200, CompanySchema)
    def get(self, query_args):
        """회사 검색

        입력한 단어가 회사명에 포함된 회사를 검색합니다.
        자동완성 검색에 사용됩니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")
        query = query_args["query"]
        try:
            company_names = company_service().get_commanies_by_name_query(query=query)
        except NotFoundCompany:
            abort(400, message=f"can not found comapny {query}")
        return company_names[response_language]


@api.route("/companies/<string:company_name>/tags")
class CompanyTags(MethodView):
    @api.arguments(
        schema=NewTagSchema(many=True),
        example=[
            {
                "tag_name": {
                    "ko": "태그_4",
                    "tw": "tag_4",
                    "en": "tag_4",
                }
            },
        ],
    )
    @api.arguments(schema=CompanyNameSchema, location="path", as_kwargs=True)
    @api.response(200, CompanySchema)
    def put(self, tags, company_name):
        """태그 추가

        회사 정보에 다수의 태그를 추가합니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")

        company_tags = []
        for tag in tags:
            for language, name in tag["tag_name"].items():
                group_id = int(name.split("_")[-1])
                company_tags.append(
                    CompanyTagDTO(language=language, name=name, group_id=group_id)
                )
        try:
            company_data = company_service().add_company_tags(
                company_name=company_name,
                tags=company_tags,
            )
        except DuplicatedTag as e:
            tag_name = e.args[0]
            abort(400, message=f"duplicated {tag_name}")

        return company_data[response_language]


@api.route("/companies/<string:company_name>/tags/<string:tag_name>")
class CompanyTagByName(MethodView):
    @api.arguments(schema=CompanyTagDeleteSchema, location="path", as_kwargs=True)
    @api.response(200, CompanySchema)
    def delete(self, company_name, tag_name):
        """태그 삭제

        태그와 회사명이 일차하는 태그 정보를 삭제합니다.
        태그 추가를 `태그_4`, `tag_4`, `タグ_4` 와 같이했다면
        `태그_4` 삭제시 모두 삭제됩니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")
        try:
            company_data = company_service().delete_company_tag(
                company_name=company_name,
                tag_name=tag_name,
            )
        except NotFoundCompanyTag as e:
            tag_name = e.args[0]
            abort(400, message=f"not found tag {tag_name} of {company_name}")

        return company_data[response_language]


@api.route("/tags")
class CompanyTagByTag(MethodView):
    @api.arguments(CompanyQueryArgsSchema, location="query")
    @api.response(200, CompanySchema)
    def get(self, query_args):
        """태그로 회사 검색

        태그가 포함된 회사를 검색합니다.
        `/tags?query=word` 와 같이 검색어를 전달해야 합니다.<br>
        headers에 `{'x-wanted-language': 'ko' }`와 같이 
        요청 언어정보가 포함되어야 합니다.
        ---
        """
        response_language = request.headers.get("X-Wanted-Language")
        tag_name = query_args["query"]
        try:
            company_names = company_service().get_commanies_by_tag(
                tag_name=tag_name,
                response_language=response_language,
            )
        except NotFoundCompany:
            abort(400, message=f"can not found comapny {tag_name}")
        return company_names
