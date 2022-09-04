import abc
from typing import Optional, Sequence

from sqlalchemy.orm.session import Session

from app.model.company import Company, CompanyName, CompanyTag


class CompanyRepository(abc.ABC):
    @abc.abstractmethod
    def get_commany_name_by_name(
        self, session: Session, **parameters
    ) -> Optional[CompanyName]:
        pass

    def search_commany_name_by_query(
        self, session: Session, **parameters
    ) -> Sequence[CompanyName]:
        pass

    def get_commany_tag_group_by_name_and_tag(
        self, session: Session, **parameters
    ) -> Optional[CompanyName]:
        pass


class SQLAlchemyCompanyRepository(CompanyRepository):
    def get_commany_name_by_name(
        self,
        session: Session,
        name: str,
    ) -> Optional[CompanyName]:
        return session.query(CompanyName).filter(CompanyName.name == name).one_or_none()

    def search_commany_names_by_query(
        self,
        session: Session,
        query: str,
        language: str,
    ) -> Sequence[CompanyName]:
        return (
            session.query(CompanyName)
            .filter(
                CompanyName.language == language,
                CompanyName.name.like(f"%{query}%"),
            )
            .all()
        )

    def get_commany_tag_group_by_name_and_tag(
        self,
        session: Session,
        company_name: str,
        tag_name: str,
    ) -> Optional[CompanyTag]:
        company_tag = (
            session.query(
                CompanyTag.group_id,
                CompanyTag.company_uuid,
            )
            .join(Company, Company.uuid == CompanyTag.company_uuid)
            .join(CompanyName, CompanyName.company_uuid == Company.uuid)
            .filter(
                CompanyName.name == company_name,
                CompanyTag.name == tag_name,
            )
            .cte()
        )

        return (
            session.query(CompanyTag)
            .filter(
                CompanyTag.group_id == company_tag.c.group_id,
                CompanyTag.company_uuid == company_tag.c.company_uuid,
            )
            .all()
        )
