from entidades.keyword import Keyword

class RepoKeyword:
    @staticmethod
    def guardar(kw: Keyword, conn):
        with conn.cursor() as cur:
            # 1) Si ya existe el texto, reciclamos su ID
            cur.execute("SELECT keyword_id FROM keywords WHERE keyword = %s;", (kw.keyword,))
            row = cur.fetchone()
            if row:
                kw_id = row[0]
            else:
                # 2) Generamos nuevo ID secuencial
                cur.execute("SELECT COALESCE(MAX(keyword_id), 0) + 1 FROM keywords;")
                kw_id = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO keywords(keyword_id, keyword, keyword_type_id)
                    VALUES (%s, %s, %s)
                """, (kw_id, kw.keyword, kw.keyword_type_id))
            return kw_id
