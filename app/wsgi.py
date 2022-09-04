from flask import Flask

from flask_smorest import Api

from app.resource.company import api as company_api


def ping():
    return (
        "pong",
        200,
        {
            "Content-Type": "text/plain",
        },
    )


def create_wsgi_app() -> Flask:
    app = Flask(__name__)
    app.route("/ping/")(ping)
    app.config["API_TITLE"] = "wanted search API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.secret_key = "__WANTED__"
    api = Api(app)
    api.register_blueprint(company_api)
    return app
