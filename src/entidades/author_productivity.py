from dataclasses import dataclass

@dataclass
class AuthorProductivity:
    author_scopus_id: str  # FK → authors.author_scopus_id
    year: int
    hindex: int
    publications_count: int
    cites_count: int
