from collections import defaultdict
from typing import List

from app.repository.commany import CompanyRepository
from app.orm import session_scope
from app.model.company import Company, CompanyName, CompanyTag
from app.service.dto.company import CompanyNameDTO, CompanyTagDTO
from app.exception import (
    DuplicatedName,
    NotFoundCompany,
    NotFoundCompanyTag,
)


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        sessionmaker,
    ):
        self.company_repository = company_repository
        self.sessionmaker = sessionmaker

    def get_all(self):
        with session_scope(self.sessionmaker) as session:
            companies = session.query(Company).all()
            datas = []
            for company in companies:
                data = self._serialize_company(company)
                data["uuid"] = str(company.uuid)
                datas.append(data)
            return datas

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

    def _serialize_company(self, company: Company) -> dict:
        company_data = defaultdict(dict)
        for name in company.names:
            company_data[name.language]["company_name"] = name.name
            company_data[name.language]["tags"] = []

        sorted_tags = sorted(company.tags, key=lambda tag: tag.group_id)
        for tag in sorted_tags:
            if not company_data[tag.language]:
                company_data[tag.language]["tags"] = []

            company_data[tag.language]["tags"].append(tag.name)
        return company_data

    def add_commany(
        self,
        names: List[CompanyNameDTO],
        tags: List[CompanyTagDTO],
    ) -> dict:
        with session_scope(self.sessionmaker) as session:
            company = Company()
            session.add(company)

            for name_dto in names:
                if self.is_name_exists(
                    name=name_dto.name,
                    language=name_dto.language,
                ):
                    raise DuplicatedName(name_dto)

                name = CompanyName(language=name_dto.language, name=name_dto.name)
                company.names.append(name)
                session.add(name)

            for tag_dto in tags:
                tag = CompanyTag(
                    language=tag_dto.language,
                    name=tag_dto.name,
                    group_id=tag_dto.group_id,
                )
                company.tags.append(tag)
                session.add(tag)

            return self._serialize_company(company)

    def get_commany_by_name(
        self,
        name: str,
    ) -> dict:
        with session_scope(self.sessionmaker) as session:
            company_name = self.company_repository.get_commany_name_by_name(
                session=session,
                name=name,
            )

            if not company_name:
                raise NotFoundCompany(name)

            company = company_name.company
            return self._serialize_company(company)

    def search_commany_by_query(
        self,
        query: str,
        language: str,
    ) -> List[dict]:
        with session_scope(self.sessionmaker) as session:
            company_names = self.company_repository.search_commany_names_by_query(
                session=session,
                query=query,
                language=language,
            )
            if not company_names:
                raise NotFoundCompany(query)

            return [
                {"company_name": company_name.name} for company_name in company_names
            ]

    def delete_company_by_name(self, name: str):
        with session_scope(self.sessionmaker) as session:
            company_name = self.company_repository.get_commany_name_by_name(
                session=session,
                name=name,
            )
            if company_name:
                company = company_name.company
                session.delete(company)

    def add_company_tags(
        self,
        company_name: str,
        tags: List[CompanyTagDTO],
    ) -> dict:
        with session_scope(self.sessionmaker) as session:
            company_name = self.company_repository.get_commany_name_by_name(
                session=session,
                name=company_name,
            )
            if not company_name:
                raise NotFoundCompany(company_name)

            company = company_name.company
            company_tags = company.tags
            for tag_dto in tags:
                if list(
                    filter(
                        lambda x: (
                            x.name == tag_dto.name and x.language == tag_dto.language
                        ),
                        company_tags,
                    )
                ):
                    continue

                tag = CompanyTag(
                    language=tag_dto.language,
                    name=tag_dto.name,
                    group_id=tag_dto.group_id,
                )
                company.tags.append(tag)
                session.add(tag)

            return self._serialize_company(company=company)

    def delete_company_tag(self, company_name: str, tag_name: str) -> dict:
        with session_scope(self.sessionmaker) as session:
            company_tags = (
                self.company_repository.get_commany_tag_group_by_name_and_tag(
                    session=session,
                    company_name=company_name,
                    tag_name=tag_name,
                )
            )
            if not company_tags:
                raise NotFoundCompanyTag(tag_name)

            company = None
            for tag in company_tags:
                if not company:
                    company = tag.company

                session.delete(tag)
            return self._serialize_company(company=company)
