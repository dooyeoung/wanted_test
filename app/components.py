import functools

from flask import current_app

from app.repository.commany import SQLAlchemyCompanyRepository
from app.service.company import CompanyService
from app.orm import database_sessionmaker


def component(func):
    """
    Component의 라이프사이클을 관리하기 위한 Decorator입니다.
    해당 Decorator는 Component객체의 생성을 캐시하여 앱의 메모리 사용을 최적화 합니다.
    `components`는 자유변수이며 Component들을 캐싱하여 담아두는 용도로 사용됩니다.
    """

    components = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__

        if name not in components:
            components[name] = func(*args, **kwargs)

        return components[name]

    return wrapper


@component
def company_repository():
    return SQLAlchemyCompanyRepository()


@component
def company_service():
    return CompanyService(
        company_repository=company_repository(),
        sessionmaker=database_sessionmaker(current_app.config["DATABASE"]),
    )
