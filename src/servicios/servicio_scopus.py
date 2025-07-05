import pybliometrics
pybliometrics.init()
import re

from pybliometrics.scopus import AuthorRetrieval, AbstractRetrieval 
from bd.bd_conexion import conexion
from entidades.author import Author
from entidades.paper import Paper
from entidades.paper_author import PaperAuthor
from entidades.source import Source     
from entidades.keyword import Keyword
from entidades.keyword_type import KeywordType     
from entidades.paper_keyword import PaperKeyword

from repos.repo_author import RepoAuthor
from repos.repo_paper import RepoPaper
from repos.repo_paper_author import RepoPaperAuthor
from repos.repo_source import RepoSource      
from repos.repo_keyword import RepoKeyword
from repos.repo_keyword_type import RepoKeywordType
from repos.repo_paper_keyword import RepoPaperKeyword

#Servicio para obtener información de un autor en Scopus y guardar en la base de datos
#Este servicio utiliza la librería pybliometrics para interactuar con la API de Scopus.
def servicioScopus(auid: str):
    conn = conexion()
    cur = conn.cursor() 
    try:
        cur.execute("BEGIN;")

        #AUTHOR
        author = AuthorRetrieval(auid)
        au = Author(
            author_scopus_id   = author.identifier,
            cvu                = None,
            author_scopus_name = author.indexed_name,
            orcid              = author.orcid,
            cites_by_documents = author.document_count,
            cites_by_authors   = author.cited_by_count
        )
        RepoAuthor.guardar(au, conn)

        author_kt_id = RepoKeywordType.guardar(
            KeywordType(keyword_type_id=0, name="Por Autor"), conn
        )
        scopus_kt_id = RepoKeywordType.guardar(
            KeywordType(keyword_type_id=0, name="Por Scopus"), conn
        )

        #PUBLICACIONES (PAPERS)
        docs = author.get_documents(refresh=True)
        for idx, doc in enumerate(docs, start=1): # se recorre cada documento del autor

            #Insertar o actualizar la fuente correspondiente
            src = Source(
                source_id        = doc.source_id,
                publication_name = getattr(doc, "publicationName", None),
                issn             = getattr(doc, "issn", None),
                eissn            = getattr(doc, "eIssn", None),
                aggregation_type = getattr(doc, "aggregationType", None)
            )
            RepoSource.guardar(src, conn)
            
            openA = doc.openaccess 
            if openA == 0:
                openA = "No"
            else:
                openA = "Si" 

            accesoFree = doc.freetoread or "No"
            
           

            accesoFreeL = doc.freetoreadLabel or ("Acceso libre" if openA == "Si" else "Acceso limitado")
            
            #Mapear y guardar Paper
            p = Paper(
                eid                 = doc.eid,
                source_id           = doc.source_id,
                authors_ids         = doc.author_ids or None,
                doi                 = doc.doi,
                pii                 = doc.pii,
                pubmed              = doc.pubmed_id,
                title               = doc.title,
                subtype             = doc.subtype,
                subtype_description = getattr(doc, "subtypeDescription", None),
                author_count        = doc.author_count,
                year                = int(getattr(doc, "coverDate","")[:4] or 0),
                cover_date          = doc.coverDate,
                cover_display_date  = doc.coverDisplayDate,
                volume              = doc.volume,
                issue_identifier    = getattr(doc, "issueIdentifier", None),
                article_number      = getattr(doc, "article_number", None),
                page_range          = getattr(doc, "pageRange", None),
                description         = doc.description,
                authkeywords        = doc.authkeywords,
                citedby_count       = doc.citedby_count,
                openaccess          = openA,
                freetoread          = accesoFree,
                freetoread_label    = accesoFreeL
            )
            RepoPaper.guardar(p, conn)


            #Relación PaperAuthor
            pa = PaperAuthor(
                paper_author_id   = idx,
                eid               = doc.eid,
                authors_scopus_id = au.author_scopus_id,
                is_creator        = bool(doc.creator)
            )
            RepoPaperAuthor.guardar(pa, conn)

           #Por Autor (las que escribe el autor en doc.authkeywords)
            raw_auth = doc.authkeywords or ""
            for palabra in [w.strip() for w in re.split(r"[;,]", raw_auth) if w.strip()]:
                kw_id = RepoKeyword.guardar(
                    Keyword(keyword_id=0, keyword=palabra, keyword_type_id=author_kt_id),
                    conn
                )
                RepoPaperKeyword.guardar(
                    PaperKeyword(eid=doc.eid, keyword_id=kw_id),
                    conn
                )

            #keywords generadas por Scopus, con AbstractRetrieval
            abs_doc = AbstractRetrieval(doc.eid, view="META_ABS")
            for palabra in abs_doc.idxterms or []:
                palabra = palabra.strip()
                if not palabra:
                    continue
                kw_id = RepoKeyword.guardar(
                    Keyword(keyword_id=0, keyword=palabra, keyword_type_id=scopus_kt_id),
                    conn
                )
                RepoPaperKeyword.guardar(
                    PaperKeyword(eid=doc.eid, keyword_id=kw_id),
                    conn
                )

        cur.execute("COMMIT;")
    except Exception:
        cur.execute("ROLLBACK;")
        raise # raise significa que se vuelve a lanzar la excepción 
    finally:
        cur.close()
        conn.close()
