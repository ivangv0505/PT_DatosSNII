from entidades.paper_keyword import PaperKeyword

class RepoPaperKeyword:
    @staticmethod
    def guardar(pk: PaperKeyword, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO papers_keywords(eid, keyword_id)
                VALUES (%s, %s)
                ON CONFLICT (eid, keyword_id) DO NOTHING;  
            """, (pk.eid, pk.keyword_id))
