from entidades.keyword import Keyword

class RepoKeyword:
    @staticmethod
    def guardar(kw: Keyword, conn) -> int:
        
        # Busca un keyword por (texto + tipo). Si existe devuelve su ID.
        # Si no existe, genera uno nuevo, lo inserta y lo devuelve.

        with conn.cursor() as cur:
            #Intenta recuperar por palabra y tipo
            cur.execute("""
                SELECT keyword_id
                  FROM keywords
                 WHERE keyword = %s
                   AND keyword_type_id = %s;
            """, (kw.keyword, kw.keyword_type_id))
            row = cur.fetchone()
            if row:
                return row[0]

            #No existe: genera nuevo ID
            cur.execute("SELECT COALESCE(MAX(keyword_id),0) + 1 FROM keywords;")
            new_id = cur.fetchone()[0]

            #Inserta(texto, tipo)
            cur.execute("""
                INSERT INTO keywords (keyword_id, keyword, keyword_type_id)
                     VALUES (%s, %s, %s);
            """, (new_id, kw.keyword, kw.keyword_type_id))

            return new_id

