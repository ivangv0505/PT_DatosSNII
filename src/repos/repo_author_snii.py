from entidades.author_sni_info import AuthorSniInfo

class RepoAuthorsniInfo:
    @staticmethod
    def guardar(asi: AuthorSniInfo, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO authorssni_info (
                  cvu, start_year, end_year, category,
                  area, discipline, subdiscipline,
                  speciality, affilation, country,
                  state, federal_entity
                ) VALUES (
                  %s, %s, %s, %s,
                  %s, %s, %s,
                  %s, %s, %s,
                  %s, %s
                )
                ON CONFLICT (cvu, start_year) DO UPDATE
                  SET end_year        = EXCLUDED.end_year,
                      category        = EXCLUDED.category,
                      area            = EXCLUDED.area,
                      discipline      = EXCLUDED.discipline,
                      subdiscipline   = EXCLUDED.subdiscipline,
                      speciality      = EXCLUDED.speciality,
                      affilation      = EXCLUDED.affilation,
                      country         = EXCLUDED.country,
                      state           = EXCLUDED.state,
                      federal_entity  = EXCLUDED.federal_entity;
            """, (
                asi.cvu,
                asi.start_year,
                asi.end_year,
                asi.category,
                asi.area,
                asi.discipline,
                asi.subdiscipline,
                asi.speciality,
                asi.affilation,
                asi.country,
                asi.state,
                asi.federal_entity
            ))