from dataclasses import dataclass
from typing import Optional 

@dataclass 
class Source:
    source_id: str               # PK
    publication_name: Optional[str]
    issn: Optional[str]
    eissn: Optional[str]
    aggregation_type: Optional[str]
