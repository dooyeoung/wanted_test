import pytest
import csv

from app.wsgi import create_wsgi_app
from app.orm import Base, database_engine
from app.components import company_service
from app.service.dto.company import CompanyNameDTO, CompanyTagDTO


def get_app():
    app = create_wsgi_app()
    app.config.from_object("app.config.TestConfig")
    return app


def pytest_sessionstart(session):
    app = get_app()
    engine = database_engine(app.config["DATABASE"])
    connection = engine.connect()
    metadata = Base.metadata
    metadata.create_all(bind=connection)
    with app.app_context():
        insert_test_data(app)


def pytest_sessionfinish(session, exitstatus):
    app = get_app()
    engine = database_engine(app.config["DATABASE"])
    connection = engine.connect()
    metadata = Base.metadata
    metadata.drop_all(bind=connection)


def insert_test_data(app):
    company_service().get_all()
    csvfile = open("wanted_temp_data.csv", "r")
    reader = csv.DictReader(csvfile)
    for row in reader:
        company_ko = row["company_ko"]
        company_en = row["company_en"]
        company_ja = row["company_ja"]

        names = []
        if company_ko:
            name = CompanyNameDTO(name=company_ko, language="ko")
            names.append(name)
        if company_en:
            name = CompanyNameDTO(name=company_en, language="en")
            names.append(name)
        if company_ja:
            name = CompanyNameDTO(name=company_ja, language="ja")
            names.append(name)

        tags = []
        tag_kos = row["tag_ko"].split("|")
        tag_ens = row["tag_en"].split("|")
        tag_jas = row["tag_ja"].split("|")
        for tag_ko, tag_en, tag_ja in zip(tag_kos, tag_ens, tag_jas):
            group_id = int(tag_ko.split("_")[-1])
            tag = CompanyTagDTO(name=tag_ko, language="ko", group_id=group_id)
            tags.append(tag)
            tag = CompanyTagDTO(name=tag_en, language="en", group_id=group_id)
            tags.append(tag)
            tag = CompanyTagDTO(name=tag_ja, language="jp", group_id=group_id)
            tags.append(tag)
        company_service().add_commany(names, tags)
    csvfile.close()


@pytest.fixture
def app():
    return get_app()


@pytest.fixture
def api(app):
    return app.test_client()
