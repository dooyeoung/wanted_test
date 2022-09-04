import argparse

from app.wsgi import create_wsgi_app

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-H", "--host", default="0.0.0.0")
parser.add_argument(
    "-p", "--port", type=int, default=9999, help="port number to listen"
)
parser.add_argument("-e", "--env", default="dev")


def main():
    args = parser.parse_args()
    wsgi_app = create_wsgi_app()

    if args.env == "prod":
        wsgi_app.config.from_object("app.config.ProductionConfig")
    elif args.env == "test":
        wsgi_app.config.from_object("app.config.TestConfig")

    wsgi_app.run(host=args.host, port=args.port, debug=True)


if __name__ == "__main__":
    main()
