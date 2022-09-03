import uuid

from sqlalchemy.schema import Column, ForeignKey
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
    names = relationship("CompanyName", backref="company", cascade="delete")
    tags = relationship("CompanyTag", backref="company", cascade="delete")


class CompanyName(Base):
    __tablename__ = "company_name"

    uuid = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    company_uuid = Column(UUIDType, ForeignKey("company.uuid", ondelete="CASCADE"))
    name = Column(String(length=20), nullable=False)
    language = Column(String(length=2), nullable=False)

    def __repr__(self) -> str:
        return f"{str(self.uuid), str(self.company_uuid), self.name, self.language}"


class CompanyTag(Base):
    __tablename__ = "company_tag"

    uuid = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    company_uuid = Column(UUIDType, ForeignKey("company.uuid", ondelete="CASCADE"))
    name = Column(String(length=20), nullable=False)
    language = Column(String(length=2), nullable=False)

    def __repr__(self) -> str:
        return f"{str(self.uuid), str(self.company_uuid), self.name, self.language}"
