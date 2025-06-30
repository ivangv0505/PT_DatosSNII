from entidades.paper import Paper

class RepoPaper:
    @staticmethod
    def guardar(p: Paper, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO papers (
                  eid, source_id, authors_ids,
                  doi, pii, pubmed,
                  title, subtype, subtype_description,
                  author_count, year, cover_date,
                  cover_display_date, volume, issue_identifier,
                  article_number, page_range, description,
                  authkeywords, citedby_count,
                  openaccess, freetoread, freetoread_label
                ) VALUES (
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s
                )
                ON CONFLICT (eid) DO UPDATE
                  SET authors_ids         = EXCLUDED.authors_ids,
                      doi                 = EXCLUDED.doi,
                      pii                 = EXCLUDED.pii,
                      pubmed              = EXCLUDED.pubmed,
                      title               = EXCLUDED.title,
                      subtype             = EXCLUDED.subtype,
                      subtype_description = EXCLUDED.subtype_description,
                      author_count        = EXCLUDED.author_count,
                      year                = EXCLUDED.year,
                      cover_date          = EXCLUDED.cover_date,
                      cover_display_date  = EXCLUDED.cover_display_date,
                      volume              = EXCLUDED.volume,
                      issue_identifier    = EXCLUDED.issue_identifier,
                      article_number      = EXCLUDED.article_number,
                      page_range          = EXCLUDED.page_range,
                      description         = EXCLUDED.description,
                      authkeywords        = EXCLUDED.authkeywords,
                      citedby_count       = EXCLUDED.citedby_count,
                      openaccess          = EXCLUDED.openaccess,
                      freetoread          = EXCLUDED.freetoread,
                      freetoread_label    = EXCLUDED.freetoread_label;
            """, (
                p.eid, p.source_id, p.authors_ids,
                p.doi, p.pii, p.pubmed,
                p.title, p.subtype, p.subtype_description,
                p.author_count, p.year, p.cover_date,
                p.cover_display_date, p.volume, p.issue_identifier,
                p.article_number, p.page_range, p.description,
                p.authkeywords, p.citedby_count,
                p.openaccess, p.freetoread, p.freetoread_label
            ))
