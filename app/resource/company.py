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
    def get(self):
        companies = company_service().get_all()
        return companies

    @api.arguments(schema=NewCompanySchema)
    @api.response(200, CompanySchema)
    def post(self, new_company):
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
        response_language = request.headers.get("X-Wanted-Language")
        company_name = path_parameter["company_name"]
        try:
            company_data = company_service().get_commany_by_name(name=company_name)
        except NotFoundCompany:
            abort(404, message=f"can not found comapny {company_name}")
        return company_data[response_language]

    @api.response(200)
    def delete(self, company_name):
        company_service().delete_company_by_name(name=company_name)
        return {"result": "success"}


@api.route("/search")
class SearchCompanies(MethodView):
    @api.arguments(CompanyQueryArgsSchema, location="query")
    def get(self, query_args):
        language = request.headers.get("X-Wanted-Language")
        query = query_args["query"]
        try:
            company_names = company_service().search_commany_by_query(
                query=query,
                language=language,
            )
        except NotFoundCompany:
            abort(400, message=f"can not found comapny {query}")
        return company_names


@api.route("/companies/<string:company_name>/tags")
class CompanyTags(MethodView):
    @api.arguments(schema=NewTagSchema(many=True))
    @api.arguments(schema=CompanyNameSchema, location="path", as_kwargs=True)
    def put(self, tags, company_name):
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
    def delete(self, company_name, tag_name):
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
