from entidades.source import Source

class RepoSource:
    @staticmethod
    def guardar(source: Source, conn):
        with conn.cursor() as cur:
            # En caso de conflicto en source_id:
            # Actualiza los datos (issn, eIssn, nombre, tipo) con los más recientes
            cur.execute("""
                INSERT INTO sources (
                  source_id,
                  publication_name,
                  issn,
                  eissn,
                  aggregation_type
                ) VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (source_id) DO UPDATE
                  SET publication_name  = EXCLUDED.publication_name,
                      issn              = EXCLUDED.issn,
                      eissn             = EXCLUDED.eissn,
                      aggregation_type  = EXCLUDED.aggregation_type;
            """, (
                source.source_id,
                source.publication_name,
                source.issn,
                source.eissn,
                source.aggregation_type
            ))
