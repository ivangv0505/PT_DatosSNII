from entidades.paper_author import PaperAuthor

class RepoPaperAuthor:
    @staticmethod
    def guardar(paAU: PaperAuthor, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO papers_authors (
                  paper_author_id, eid,
                  authors_scopus_id, is_creator
                ) VALUES (%s,%s,%s,%s)
                ON CONFLICT DO NOTHING; 
            """, (      # no se hace nada, porque la tabla es una tabla de relación
                        # cuyo único propósito es registrar si un autor ya está asociado a un paper
                paAU.paper_author_id,
                paAU.eid,
                paAU.authors_scopus_id,
                paAU.is_creator
            ))
