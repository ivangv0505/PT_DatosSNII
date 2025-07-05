from dataclasses import dataclass

@dataclass
class AuthorPapersCites:
    author_scopus_id: str  
    eid: str               
    year: int
    cites_count: int
