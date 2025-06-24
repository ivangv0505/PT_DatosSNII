import json
import pybliometrics
#abstractretrieval sirve para recuperar info de articulos, AuthorRetrieval es para autores,
#ScopusSearch es para buscar articulos por auid
from pybliometrics.scopus import AuthorRetrieval, ScopusSearch, AbstractRetrieval 

from bd_consultas import author_and_papers


#Inicializa la API de Scopus
pybliometrics.init()

auid = input("Introduce el Scopus Author ID (auid): ").strip()

#Recupera JSON del autor
author = AuthorRetrieval(auid)
author_json = author._json
orcid = author.orcid 


print("ORCiD obtenido:", orcid)
print(json.dumps(author_json, indent=2, ensure_ascii=False))


#Imprime el JSON completo del autor
print("\n=== JSON de AUTOR obtenido ===")
print(json.dumps(author_json, indent=2, ensure_ascii=False))

#Busca todos los EIDs del autor
search = ScopusSearch(f"AU-ID({auid})", subscriber=False)
eids   = [res.eid for res in search.results]

#Imprime la lista de EIDs que se procesan
print(f"\nEIDs encontrados para {auid}: {eids}")

#Para cada EID, recupera el JSON completo del paper
articles_json = []
for i, eid in enumerate(eids, start=1):
    ab = AbstractRetrieval(eid, view="FULL", id_type="eid")
    art_json = ab._json
    articles_json.append(art_json)
    #Imprime el JSON completo de este paper
    print(f"\n=== JSON de PAPER {i} (EID={eid}) ===")
    print(json.dumps(art_json, indent=2, ensure_ascii=False))

# with open(f"author_{auid}.json", "w", encoding="utf-8") as f:
#     json.dump(author_json, f, ensure_ascii=False, indent=2)
# for i, art in enumerate(articles_json, start=1):
#     with open(f"paper_{i}.json", "w", encoding="utf-8") as f:
#         json.dump(art, f, ensure_ascii=False, indent=2)

#Llamar a nuestra función de inserción en BD
author_and_papers(author_json, articles_json, orcid)
