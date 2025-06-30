from entidades.author import Author

class RepoAuthor:
    @staticmethod
    def guardar(author: Author, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO authors (
                  author_scopus_id, cvu,
                  author_scopus_name, ORCID,
                  cites_by_documents, cites_by_authors
                ) VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT (author_scopus_id) DO UPDATE
                  SET cvu                 = EXCLUDED.cvu,
                      author_scopus_name  = EXCLUDED.author_scopus_name,
                      ORCID               = EXCLUDED.ORCID,
                      cites_by_documents  = EXCLUDED.cites_by_documents,
                      cites_by_authors    = EXCLUDED.cites_by_authors;
            """, (
                author.author_scopus_id,
                author.cvu,
                author.author_scopus_name,
                author.orcid,
                author.cites_by_documents,
                author.cites_by_authors
            ))
