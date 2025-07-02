from entidades.keyword_type import KeywordType

class RepoKeywordType:
    @staticmethod
    def obtener_o_crear(name: str, conn) -> int:
        
        #Busca un keyword_type por nombre. Si existe, devuelve su ID.
        #Si no existe, le asigna el siguiente ID libre, lo inserta y lo devuelve.
        with conn.cursor() as cur:
            #Buscar si ya existe el tipo de keyword
            cur.execute(
                "SELECT keyword_type_id FROM keyword_types WHERE name = %s;",
                (name,)
            )
            row = cur.fetchone()
            if row:
                return row[0]
            #No existe, se calcula el nuevo ID
            cur.execute(
                "SELECT COALESCE(MAX(keyword_type_id), 0) + 1 FROM keyword_types;"
            )
            new_id = cur.fetchone()[0]
            #Se inserta el nuevo tipo
            cur.execute("""
                INSERT INTO keyword_types(keyword_type_id, name)
                VALUES (%s, %s);
            """, (new_id, name))
            return new_id
    @staticmethod
    def guardar(kt: KeywordType, conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO keyword_types(keyword_type_id, name)
                VALUES (%s, %s)
                ON CONFLICT (keyword_type_id) DO UPDATE
                  SET name = EXCLUDED.name;
            """, (kt.keyword_type_id, kt.name))
