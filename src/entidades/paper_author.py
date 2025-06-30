from dataclasses import dataclass

@dataclass
class PaperAuthor:
    paper_author_id: int        # PK
    eid: str                    # FK → papers
    authors_scopus_id: str      # FK → authors
    is_creator: bool
