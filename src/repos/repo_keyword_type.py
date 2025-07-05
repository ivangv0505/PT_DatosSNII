from entidades.keyword_type import KeywordType

class RepoKeywordType:
    @staticmethod
    def guardar(kt: KeywordType, conn) -> int:
        # Inserta o actualiza un KeywordType.
        # Si kt.keyword_type_id == 0: busca por name. Si existe devuelve ese ID,
        # si no existe genera un nuevo ID, lo inserta y lo devuelve.
        # Si kt.keyword_type_id != 0: hace upsert por ID y devuelve kt.keyword_type_id. 
        with conn.cursor() as cur:
            if kt.keyword_type_id == 0:
                #Ya existe un tipo con ese nombre?
                cur.execute(
                    "SELECT keyword_type_id FROM keyword_types WHERE name = %s;",
                    (kt.name,)
                )
                row = cur.fetchone()
                if row:
                    return row[0]
                #No existe: calculamos un nuevo ID
                cur.execute(
                    "SELECT COALESCE(MAX(keyword_type_id),0) + 1 FROM keyword_types;"
                )
                new_id = cur.fetchone()[0]
                #Insertamos el nuevo tipo
                cur.execute("""
                    INSERT INTO keyword_types(keyword_type_id, name)
                    VALUES (%s, %s);
                """, (new_id, kt.name))
                return new_id
            else:
                #Ya tenemos un ID válido: upsert para actualizar el name si cambió
                cur.execute("""
                    INSERT INTO keyword_types(keyword_type_id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (keyword_type_id) DO UPDATE
                      SET name = EXCLUDED.name;
                """, (kt.keyword_type_id, kt.name))
                return kt.keyword_type_id

