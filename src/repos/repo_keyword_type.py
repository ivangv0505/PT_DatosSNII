from entidades.keyword_type import KeywordType

class RepoKeywordType:
    @staticmethod
    def guardar(kt: KeywordType, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO keyword_types(keyword_type_id, name)
                VALUES (%s, %s)
                ON CONFLICT (keyword_type_id) DO UPDATE
                  SET name = EXCLUDED.name;
            """, (kt.keyword_type_id, kt.name))
