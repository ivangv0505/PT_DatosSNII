from dataclasses import dataclass
from typing import Optional

@dataclass
class Author:
    author_scopus_id: str       # PK
    cvu: Optional[str]          # FK → authorssni
    author_scopus_name: Optional[str]
    orcid: Optional[str]        
    cites_by_documents: Optional[int]
    cites_by_authors: Optional[int]
