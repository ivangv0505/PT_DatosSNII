# db_queries.py
import os
import json
import psycopg2

def author_and_papers(author_json, articles_json_list, orcid):

    #Inserta/actualiza en la BD, dentro de una transacción segura
    #   1) affiliation
    #   2) authors
    #   3) authors_productivity
    #   4) sources
    #   5) papers
    #   6) papers_authors
    #   7) papers_authors_affiliations
    
    #pasa dict/list → JSON string, deja int/str/bool tal cual
    def safe(val):
        if val is None or isinstance(val, (str, int, float, bool)):
            return val
        return json.dumps(val, ensure_ascii=False)

    #Extraer campos del autor
    core    = author_json.get("coredata", {})
    profile = author_json.get("author-profile", {})
    auid    = core.get("dc:identifier", "").split(":")[-1]
    name    = profile.get("preferred-name", {}).get("indexed-name")
    cites_d = int(core.get("cited-by-count", 0))
    cites_a = int(core.get("citation-count",   0))
    hindex  = int(author_json.get("h-index",    0))
    docs    = int(core.get("document-count",   0))

    #Afiliación actual
    curr = (profile
            .get("affiliation-current", {})
            .get("affiliation", {})
            .get("ip-doc", {}))
    aff_id      = int(curr.get("@id",                0))
    aff_name    = curr.get("preferred-name", {}).get("$")
    aff_city    = curr.get("address", {}).get("city")
    aff_country = curr.get("address", {}).get("country")

    #Conexión
    conn = psycopg2.connect(
        dbname   = os.getenv("DB_NAME",   "datossnii"),
        user     = os.getenv("DB_USER",   "postgres"),
        password = os.getenv("DB_PASS",   "pt050505"),
        host     = os.getenv("DB_HOST",   "localhost"),
        port     = os.getenv("DB_PORT",   "5432")
    )
    cur = conn.cursor()

    try:
        #BEGIN: inicio de transacción
        cur.execute("BEGIN;")

        #affiliation
        cur.execute("""
            INSERT INTO affiliation (
              affilation_id, affilation_name,
              affilation_city, affilation_country
            ) VALUES (%s,%s,%s,%s)
            ON CONFLICT (affilation_id) DO UPDATE
              SET affilation_name    = EXCLUDED.affilation_name,
                  affilation_city    = EXCLUDED.affilation_city,
                  affilation_country = EXCLUDED.affilation_country;
        """, (aff_id, aff_name, aff_city, aff_country))

        #authors
        cur.execute("""
            INSERT INTO authors (
              author_scopus_id, cvu,
              author_scopus_name, ORCID,
              cites_by_documents, cites_by_authors
            ) VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (author_scopus_id) DO UPDATE
              SET author_scopus_name  = EXCLUDED.author_scopus_name,
                  ORCID              = EXCLUDED.ORCID,
                  cites_by_documents  = EXCLUDED.cites_by_documents,
                  cites_by_authors    = EXCLUDED.cites_by_authors;
        """, (auid, None, name, orcid, cites_d, cites_a))

        #authors_productivity
        cur.execute("""
            INSERT INTO authors_productivity (
              author_scopus_id, year,
              hindex, publications_count, cites_count
            ) VALUES (
              %s, EXTRACT(YEAR FROM CURRENT_DATE)::INT,
              %s, %s, %s
            )
            ON CONFLICT (author_scopus_id, year) DO UPDATE
              SET hindex             = EXCLUDED.hindex,
                  publications_count = EXCLUDED.publications_count,
                  cites_count        = EXCLUDED.cites_count;
        """, (auid, hindex, docs, cites_d))

        #sources + papers + relaciones
        for art in articles_json_list:
            c = art.get("coredata", {})

            # sources
            params_src = [
                c.get("source-id"),
                c.get("prism:publicationName"),
                c.get("prism:issn"),
                c.get("prism:eissn"),
                c.get("prism:aggregationType")
            ]
            cur.execute("""
                INSERT INTO sources (
                  source_id, publication_name,
                  issn, eissn, aggregation_type
                ) VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (source_id) DO UPDATE
                  SET publication_name = EXCLUDED.publication_name,
                      issn             = EXCLUDED.issn,
                      eissn            = EXCLUDED.eissn,
                      aggregation_type = EXCLUDED.aggregation_type;
            """, [ safe(x) for x in params_src ])

            # papers
            eid        = c.get("eid")
            authors    = art.get("authors", {}).get("author", [])
            auth_ids   = ";".join(a.get("@auid","") for a in authors)
            desc       = art.get("dc:description")
            keywords   = art.get("authkeywords")
            params_pap = [
                eid,
                c.get("source-id"),
                auth_ids,
                c.get("prism:doi"),
                c.get("pii"),
                c.get("pubmed-id"),
                c.get("dc:title"),
                c.get("subtype"),
                c.get("subtypeDescription"),
                int(c.get("author-count",0)),
                int(c.get("coverDate","")[:4] or 0),
                c.get("prism:coverDate"),
                c.get("coverDisplayDate"),
                c.get("prism:volume"),
                c.get("issueIdentifier"),
                c.get("article-number"),
                c.get("pageRange"),
                desc,
                keywords,
                int(c.get("citedby-count",0)),
                c.get("openaccess"),
                c.get("freeToRead"),
                c.get("freeToReadLabel")
            ]
            cur.execute("""
                INSERT INTO papers (
                  eid, source_id, authors_ids, doi, pii, pubmed,
                  title, subtype, subtype_description,
                  author_count, year, cover_date,
                  cover_display_date, volume, issue_identifier,
                  article_number, page_range, description,
                  authkeywords, citedby_count,
                  openaccess, freetoread, freetoread_label
                ) VALUES (
                  %s,%s,%s,%s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,
                  %s,%s,
                  %s,%s,%s
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
                      volume              = EXCLUDED.volume,
                      issue_identifier    = EXCLUDED.issue_identifier,
                      article_number      = EXCLUDED.article_number,
                      page_range          = EXCLUDED.page_range,
                      description         = EXCLUDED.description,
                      authkeywords        = EXCLUDED.authkeywords,
                      citedby_count       = EXCLUDED.citedby_count;
            """, [ safe(x) for x in params_pap ])

            #papers_authors + papers_authors_affiliations
            cur.execute("SELECT COALESCE(MAX(paper_author_id),0)+1 FROM papers_authors;")
            link_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO papers_authors (
                  paper_author_id, eid, authors_scopus_id, is_creator
                ) VALUES (%s,%s,%s,%s)
                ON CONFLICT (paper_author_id) DO NOTHING;
            """, (link_id, eid, auid, True))
            cur.execute("""
                INSERT INTO papers_authors_affiliations (
                  affilation_id, paper_author_id
                ) VALUES (%s,%s)
                ON CONFLICT DO NOTHING;
            """, (aff_id, link_id))

        #COMMIT: confirma todos los cambios
        cur.execute("COMMIT;")
        print("Transacción exitosa, se guardaron los datos.")

    except Exception as e:
        #ROLLBACK: revierte si algo falla
        cur.execute("ROLLBACK;")
        print("❌ Error, se hizo ROLLBACK:", e)

    finally:
        cur.close()
        conn.close()
