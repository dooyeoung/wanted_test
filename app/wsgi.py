from flask import Flask


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

    return app
