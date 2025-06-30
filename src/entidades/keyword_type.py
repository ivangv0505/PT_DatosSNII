from dataclasses import dataclass
from typing import Optional

@dataclass
class KeywordType:
    keyword_type_id: int        # PK
    name: Optional[str]
