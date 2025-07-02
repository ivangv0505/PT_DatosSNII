from dataclasses import dataclass
from typing import Optional

@dataclass
class SourceProductivity:
    source_id: str
    year: int
    SJR: Optional[str]
    SNIP: Optional[str]
    cite_score: Optional[str]
    rank: Optional[str]
    percentile: Optional[str]
    quartile: Optional[str]
