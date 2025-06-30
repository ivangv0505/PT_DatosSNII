from dataclasses import dataclass
from typing import Optional

@dataclass
class Keyword:
    keyword_id: int             # PK
    keyword: Optional[str]
    keyword_type_id: int        # FK → keyword_types
