from entidades.author_productivity import AuthorProductivity

class RepoAuthorsProductivity:
    @staticmethod
    def guardar(ap: AuthorProductivity, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO authors_productivity (
                  author_scopus_id, year, hindex,
                  publications_count, cites_count
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (author_scopus_id, year) DO UPDATE
                  SET hindex             = EXCLUDED.hindex,
                      publications_count = EXCLUDED.publications_count,
                      cites_count        = EXCLUDED.cites_count;
            """, (
                ap.author_scopus_id,
                ap.year,
                ap.hindex,
                ap.publications_count,
                ap.cites_count
            ))