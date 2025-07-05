from dataclasses import dataclass

@dataclass
class AuthorPapersCites:
    author_scopus_id: str  # FK → authors.author_scopus_id 
    eid: str               # FK → papers.eid
    year: int
    cites_count: int
