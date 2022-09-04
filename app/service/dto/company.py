from dataclasses import dataclass


@dataclass
class CompanyNameDTO:
    name: str
    language: str


@dataclass
class CompanyTagDTO:
    name: str
    language: str
    group_id: int
