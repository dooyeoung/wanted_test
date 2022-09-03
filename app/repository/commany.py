import abc
from typing import Optional, Sequence

from sqlalchemy.orm.session import Session

from app.model.company import Company, CompanyName


class CompanyRepository(abc.ABC):
    @abc.abstractmethod
    def get_commany_name_by_name(
        self, session: Session, **parameters
    ) -> Optional[Company]:
        pass

    def search_commany_name_by_query(
        self, session: Session, **parameters
    ) -> Sequence[Company]:
        pass


class SQLAlchemyCompanyRepository(CompanyRepository):
    def get_commany_name_by_name(
        self,
        session: Session,
        name: str,
    ) -> Optional[Company]:
        return session.query(CompanyName).filter(CompanyName.name == name).one_or_none()

    def search_commany_names_by_query(
        self,
        session: Session,
        query: str,
        language: str,
    ) -> Sequence[Company]:
        return (
            session.query(CompanyName)
            .filter(
                CompanyName.language == language,
                CompanyName.name.like(f"%{query}%"),
            )
            .all()
        )
