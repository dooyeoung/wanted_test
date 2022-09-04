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

    def get_commanies_by_name_query(
        self, session: Session, **parameters
    ) -> Sequence[CompanyName]:
        pass

    def get_commanies_by_tag(
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

    def get_commanies_by_name_query(
        self,
        session: Session,
        query: str,
    ) -> Sequence[CompanyName]:
        return (
            session.query(CompanyName)
            .filter(
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

    def get_commanies_by_tag(
        self,
        session: Session,
        tag_name: str,
    ):
        return (
            session.query(CompanyName)
            .join(Company, Company.uuid == CompanyName.company_uuid)
            .join(CompanyTag, CompanyTag.company_uuid == Company.uuid)
            .filter(
                CompanyTag.name == tag_name,
            )
            .all()
        )
