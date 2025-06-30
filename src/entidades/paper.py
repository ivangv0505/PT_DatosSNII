from dataclasses import dataclass 
from datetime import date
from typing import Optional

@dataclass
class Paper:
    eid: str                    # PK
    source_id: Optional[str]    # FK → sources
    authors_ids: Optional[str]  
    doi: Optional[str]
    pii: Optional[str]
    pubmed: Optional[str]
    title: Optional[str]
    subtype: Optional[str]
    subtype_description: Optional[str]
    author_count: Optional[int]
    year: Optional[int]
    cover_date: Optional[date]
    cover_display_date: Optional[str]
    volume: Optional[str]
    issue_identifier: Optional[str]
    article_number: Optional[str]
    page_range: Optional[str]
    description: Optional[str]
    authkeywords: Optional[str]
    citedby_count: Optional[int]
    openaccess: Optional[str]
    freetoread: Optional[str]
    freetoread_label: Optional[str]
