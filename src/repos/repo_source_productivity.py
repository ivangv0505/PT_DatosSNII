from entidades.source_productivity import SourceProductivity

class RepoSourceProductivity:
    @staticmethod
    def guardar(sp: SourceProductivity, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sources_productivity (
                  source_id, year, SJR, SNIP,
                  cite_score, rank, percentile, quartile
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_id, year) DO UPDATE
                  SET SJR        = EXCLUDED.SJR,
                      SNIP       = EXCLUDED.SNIP,
                      cite_score = EXCLUDED.cite_score,
                      rank       = EXCLUDED.rank,
                      percentile = EXCLUDED.percentile,
                      quartile   = EXCLUDED.quartile;
            """, (
                sp.source_id,
                sp.year,
                sp.SJR,
                sp.SNIP,
                sp.cite_score,
                sp.rank,
                sp.percentile,
                sp.quartile
            ))