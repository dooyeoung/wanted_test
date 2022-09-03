import uuid

from sqlalchemy.schema import Column, ForeignKeyConstraint
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy_utc.sqltypes import UtcDateTime
from sqlalchemy_utils.types.uuid import UUIDType

from app.orm import Base


class Company(Base):
    __tablename__ = "company"

    uuid = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    created_at = Column(UtcDateTime, nullable=False, default=now())
    names = relationship("CompanyName", back_populates="company")
    tags = relationship("CompanyTag", back_populates="company")


class CompanyName(Base):
    __tablename__ = "company_name"

    uuid = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    company_uuid = Column(UUIDType, nullable=False)
    name = Column(String(length=20), nullable=False)
    language = Column(String(length=2), nullable=False)
    company = relationship("Company", back_populates="names")

    __table_args__ = (
        ForeignKeyConstraint(
            columns=["company_uuid"], refcolumns=[Company.uuid], ondelete="cascade"
        ),
    )

    def __repr__(self) -> str:
        return f"{str(self.uuid), str(self.company_uuid), self.name, self.language}"


class CompanyTag(Base):
    __tablename__ = "company_tag"

    uuid = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    company_uuid = Column(UUIDType, nullable=False)
    name = Column(String(length=20), nullable=False)
    language = Column(String(length=2), nullable=False)
    company = relationship("Company", back_populates="tags")

    __table_args__ = (
        ForeignKeyConstraint(
            columns=["company_uuid"], refcolumns=[Company.uuid], ondelete="cascade"
        ),
    )

    def __repr__(self) -> str:
        return f"{str(self.uuid), str(self.company_uuid), self.name, self.language}"
