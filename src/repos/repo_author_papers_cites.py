from entidades.author_papers_cites import AuthorPapersCites

class RepoAuthorPapersCites:
    @staticmethod
    def guardar(apc: AuthorPapersCites, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO authors_papers_cites (
                  author_scopus_id, eid, year, cites_count
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (author_scopus_id, eid, year) DO UPDATE
                  SET cites_count = EXCLUDED.cites_count;
            """, (
                apc.author_scopus_id,
                apc.eid,
                apc.year,
                apc.cites_count
            ))
