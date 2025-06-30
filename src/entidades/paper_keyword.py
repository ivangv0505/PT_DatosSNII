from dataclasses import dataclass

@dataclass
class PaperKeyword:
    eid: str                    # FK → papers
    keyword_id: int             # FK → keywords
