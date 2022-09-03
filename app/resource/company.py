from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint

from app.schema.company import CompanySchema
from app.orm import session_scope, database_sessionmaker
from app.model.company import Company

api = Blueprint("company", __name__, url_prefix="/company")



# companies
# tags
# search


@api.route("/")
class SearchCompany(MethodView):
    @api.response(
        200,
        CompanySchema(many=True),
        example={
            "source_url": "https://naver.com",
            "id": 1,
            "short_id": "dddddL",
        },
    )
    def get(self):
        """/

        단축 Url 조회
        ---
        """
        app_config = current_app.config
        sessionmaker=database_sessionmaker(
            app_config["DATABASE"]
        )

        with session_scope(sessionmaker) as session:
            session.query(Company).all()
        datas = []
        return datas
