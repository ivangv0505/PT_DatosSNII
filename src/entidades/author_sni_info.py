from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthorSniInfo:
    cvu: str               # FK → authorssni.cvu
    start_year: int
    end_year: int
    category: Optional[str]
    area: Optional[str]
    discipline: Optional[str]
    subdiscipline: Optional[str]
    speciality: Optional[str]
    affilation: Optional[str]
    country: Optional[str]
    state: Optional[str]
    federal_entity: Optional[str]
