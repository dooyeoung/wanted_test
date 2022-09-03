from collections import defaultdict
from typing import List

from app.repository.commany import CompanyRepository
from app.orm import session_scope
from app.model.company import Company, CompanyName, CompanyTag
from app.service.dto.company import CompanyNameDTO, CompanyTagDTO
from app.exception import DuplicatedNameException


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        sessionmaker,
    ):
        self.url_repository = company_repository
        self.sessionmaker = sessionmaker

    def get_all(self):
        with session_scope(self.sessionmaker) as session:
            companies = session.query(Company).all()
            return companies

    def is_name_exists(self, name, language) -> bool:
        with session_scope(self.sessionmaker) as session:
            return (
                session.query(CompanyName)
                .filter(
                    CompanyName.name == name,
                    CompanyName.language == language,
                )
                .first()
                is not None
            )

    def add_commany(
        self,
        names: List[CompanyNameDTO],
        tags: List[CompanyTagDTO],
    ):
        language_company_data = defaultdict(dict)

        with session_scope(self.sessionmaker) as session:
            company = Company()
            session.add(company)

            for name_dto in names:
                if self.is_name_exists(
                    name=name_dto.name,
                    language=name_dto.language,
                ):
                    raise DuplicatedNameException(name_dto)

                company_name = CompanyName(
                    company=company, language=name_dto.language, name=name_dto.name
                )
                session.add(company_name)
                language_company_data[name_dto.language]["company_name"] = name_dto.name
                language_company_data[name_dto.language]["tags"] = []

            for tag_dto in tags:
                company_tag = CompanyTag(
                    company=company, language=tag_dto.language, name=tag_dto.name
                )
                session.add(company_tag)
                language_company_data[tag_dto.language]["tags"].append(tag_dto.name)

            return language_company_data
