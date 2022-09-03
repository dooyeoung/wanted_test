from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint

from app.schema.company import (
    CompanySchema,
    NewCompanySchema,
    CompanyNameSchema,
    CompanyQueryArgsSchema,
)
from app.orm import database_sessionmaker
from app.service.dto.company import CompanyNameDTO, CompanyTagDTO
from app.service.company import CompanyService
from app.repository.commany import SQLAlchemyCompanyRepository
from app.exception import DuplicatedNameException, NotFoundCompany
from flask_smorest import abort

api = Blueprint("company", __name__, url_prefix="/")


@api.route("/companies")
class Companies(MethodView):
    def get(self):
        service = CompanyService(
            company_repository=SQLAlchemyCompanyRepository(),
            sessionmaker=database_sessionmaker(current_app.config["DATABASE"]),
        )
        companies = service.get_all()
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
                company_tags.append(CompanyTagDTO(language=language, name=name))

        try:
            service = CompanyService(
                company_repository=SQLAlchemyCompanyRepository(),
                sessionmaker=database_sessionmaker(current_app.config["DATABASE"]),
            )
            company_data = service.add_commany(
                names=company_names,
                tags=company_tags,
            )
        except DuplicatedNameException as e:
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
            service = CompanyService(
                company_repository=SQLAlchemyCompanyRepository(),
                sessionmaker=database_sessionmaker(current_app.config["DATABASE"]),
            )
            company_data = service.get_commany_by_name(name=company_name)
        except NotFoundCompany:
            abort(400, message=f"can not found comapny {company_name}")
        return company_data[response_language]


@api.route("/search")
class SearchCompanies(MethodView):
    @api.arguments(CompanyQueryArgsSchema, location="query")
    def get(self, query_args):
        language = request.headers.get("X-Wanted-Language")
        query = query_args["query"]
        try:
            service = CompanyService(
                company_repository=SQLAlchemyCompanyRepository(),
                sessionmaker=database_sessionmaker(current_app.config["DATABASE"]),
            )
            company_names = service.search_commany_by_query(
                query=query,
                language=language,
            )
        except NotFoundCompany:
            abort(400, message=f"can not found comapny {query}")
        return company_names
