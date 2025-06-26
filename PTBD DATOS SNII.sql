--Se crea la tabla sources
--Importante mencionar que esta tabla se creó primero, ya que sin fuentes no hay artículo.

CREATE TABLE sources(
    source_id VARCHAR PRIMARY KEY,  --source_id es la llave primaria que identifica de forma única a cada fuente de publicación 
    publication_name VARCHAR,  --Nombre de la publicación  
    issn VARCHAR,  --Número ISSN de la versión impresa 
    eissn VARCHAR, --Número eISSN de la versión electrónica 
    aggregation_type VARCHAR --Tipo de agregación o fuente como revista cientítica, texto científico, conferencia escrita, etc.
);
 
--Se crea la tabla papers
CREATE TABLE papers(
    eid VARCHAR PRIMARY KEY, --eid es la llave primaria que identifica de forma única cada paper 
    source_id VARCHAR, --Identificador del medio de publicación (foreign key hacia sources) 
    authors_ids VARCHAR, --Cadena que puede contener los IDs de los autores del paper 
    doi VARCHAR, --Identificador DOI del paper 
    pii VARCHAR, --Identificador PII del paper 
    pubmed VARCHAR, --Identificador PubMed del paper 
    title VARCHAR, --Título del paper 
    subtype VARCHAR, --Subtipo del artículo (ej. research-article) 
    subtype_description VARCHAR, -- Descripción del subtipo del artículo 
    author_count INT, --Cantidad de autores que participaron en el paper 
    year INT, --Año de publicación del paper 
    cover_date DATE, --Fecha de portada de la publicación 
    cover_display_date VARCHAR, --Fecha mostrada de forma textual (ej. Marzo 2002) 
    volume VARCHAR, --Volumen de la publicación 
    issue_identifier VARCHAR, --Número de edición o fascículo 
    article_number VARCHAR, --Número del artículo dentro de la publicación 
    page_range VARCHAR, --Rango de páginas donde se encuentra el artículo 
    description TEXT, --Descripción general del contenido del paper 
    authkeywords TEXT, --Palabras clave del autor para el artículo 
    citedby_count INT, --Número de veces que el artículo ha sido citado 
    openaccess VARCHAR, --Indica si el artículo es de acceso abierto 
    freetoread VARCHAR, --Indica si es de lectura gratuita 
    freetoread_label VARCHAR, --Etiqueta descriptiva del acceso gratuito 
    FOREIGN KEY (source_id) REFERENCES sources(source_id) --La columna source_id es llave foránea que hace referencia a source_id en la tabla sources 
);

--Se crea la tabla affiliation
CREATE TABLE affiliation(
    affilation_id INT PRIMARY KEY, --affilation_id es la llave primaria que identifica de forma única a cada institución de afiliación 
    affilation_name VARCHAR, --Nombre de la institución de afiliación 
    affilation_city VARCHAR, --Ciudad en la que se encuentra la institución 
    affilation_country VARCHAR --País en el que se encuentra la institución 
);


--Se crea la tabla authorssni
CREATE TABLE authorssni(
    cvu VARCHAR PRIMARY KEY, --cvu es la llave primaria que identifica de forma única a cada autor dentro del SNI 
    names VARCHAR, --Nombres del autor 
    surnames VARCHAR, --Apellidos del autor 
    nobilis VARCHAR, --Título o tratamiento académico (ej. Dr., Mtro., etc.) 
    init_year INT, --Año de ingreso del autor al SNI 
    career_length INT --Duración (en años) de la carrera del autor en el SNI 
);


--Se crea la tabla authors
CREATE TABLE authors(
    author_scopus_id VARCHAR PRIMARY KEY, --author_scopus_id es la llave primaria que identifica de forma única a cada autor 
    cvu VARCHAR, --CVU del autor, se conecta con la tabla authorssni 
    author_scopus_name VARCHAR, --Nombre del autor tal como aparece en Scopus 
    ORCID VARCHAR, --Identificador ORCID del autor 
    cites_by_documents INT, --Número de citas que ha recibido el autor por documentos 
    cites_by_authors INT, --Número de citas que ha recibido el autor por parte de otros autores 
    FOREIGN KEY (cvu) REFERENCES authorssni(cvu) --La columna cvu es llave foránea que hace referencia al CVU de la tabla authorssni 
);


--Se crea la tabla papers_authors
CREATE TABLE papers_authors(
    paper_author_id INT PRIMARY KEY, --paper_author_id es la llave primaria que identifica cada relación autor-paper 
    eid VARCHAR, --Identificador del paper (llave foránea hacia la tabla papers) 
    authors_scopus_id VARCHAR, --Identificador Scopus del autor (llave foránea hacia la tabla authors) 
    is_creator BOOLEAN, --Indica si el autor es el autor principal o creador del paper 
    -- SE COMENTA REFERENCIA A PAPERS FOREIGN KEY (eid) REFERENCES papers(eid), --La columna eid es llave foránea que referencia a papers 
    FOREIGN KEY (authors_scopus_id) REFERENCES authors(author_scopus_id) --La columna authors_scopus_id es llave foránea que referencia a authors 
);

DROP TABLE IF EXISTS papers_authors CASCADE;

--Se crea la tabla keyword_types
CREATE TABLE keyword_types(
    keyword_type_id INT PRIMARY KEY, --keyword_type_id es la llave primaria que identifica el tipo de palabra clave 
    name VARCHAR --Nombre del tipo de palabra clave (por ejemplo, temática, técnica, etc.) 
);

--Se crea la tabla keywords
CREATE TABLE keywords(
    keyword_id INT PRIMARY KEY, --keyword_id es la llave primaria que identifica cada palabra clave 
    keyword VARCHAR, --Palabra clave registrada 
    keyword_type_id INT, --Tipo de palabra clave (llave foránea hacia la tabla keyword_types) 
    FOREIGN KEY (keyword_type_id) REFERENCES keyword_types(keyword_type_id) -- Relación con la tabla keyword_types 
);

--Se crea la tabla papers_keywords
CREATE TABLE papers_keywords(
    eid VARCHAR, --Identificador del paper (llave foránea hacia la tabla papers) 
    keyword_id INT, --Identificador de la palabra clave (llave foránea hacia la tabla keywords) 
    PRIMARY KEY (eid, keyword_id), --Combinación de eid y keyword_id como llave primaria compuesta 
    FOREIGN KEY (eid) REFERENCES papers(eid), --Relación con la tabla papers 
    FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id) --Relación con la tabla keywords 
);

--Se crea la tabla authors_productivity
CREATE TABLE authors_productivity(
    author_scopus_id VARCHAR, --Identidicador del autor (se conecta con authors)
    year INT, --Año de la productividad
    hindex INT, --Índice H del autor
    publications_count INT, --Número de publicaciones ese año
    cites_count INT, --Número de citas ese año
    PRIMARY KEY (author_scopus_id, year), --Llave primaria
    FOREIGN KEY (author_scopus_id) REFERENCES authors(author_scopus_id) --Llave foranea que dirigirá a authors
);


--Se crea la tabla sources_productivity
CREATE TABLE sources_productivity(
    source_id VARCHAR, --Identificador de la fuente de publicación (llave foránea hacia la tabla sources) 
    year INT, --Año en que se registran las métricas de productividad 
    SJR VARCHAR, --Indicador SCImago Journal Rank de la fuente en ese año 
    SNIP VARCHAR, --Indicador Source Normalized Impact per Paper de la fuente en ese año 
    cite_score VARCHAR, --Puntuación CiteScore de la fuente 
    rank VARCHAR, --Ranking de la fuente dentro de su categoría 
    percentile VARCHAR, --Percentil de impacto de la fuente en comparación con otras 
    quartile VARCHAR, --Cuartil (Q1, Q2, etc.) en el que se encuentra la fuente ese año 
    PRIMARY KEY (source_id, year), --Llave primaria compuesta por source_id y year 
    FOREIGN KEY (source_id) REFERENCES sources(source_id) --source_id es llave foránea que referencia a la tabla sources 
);



--Se crea la tabla papers_productivity
CREATE TABLE papers_productivity(
    eid VARCHAR, --Identificador del paper (llave foránea hacia la tabla papers) 
    year INT, --Año en que se mide la productividad o impacto del paper 
    cites_count INT, --Número de citas recibidas por el paper en ese año 
    PRIMARY KEY (eid, year), --Llave primaria compuesta por eid y year 
    FOREIGN KEY (eid) REFERENCES papers(eid) --eid es llave foránea que referencia a la tabla papers 
);

--Se crea la tabla authorssni_info
CREATE TABLE authorssni_info(
    cvu VARCHAR, --Identificador del autor en el SNI (llave foránea hacia authorssni) 
    start_year INT, --Año de inicio del registro o participación en esa categoría 
    end_year INT, --Año de finalización de la categoría o registro 
    category VARCHAR, --Categoría del autor dentro del SNI (Ej. Candidato, Nivel 1, etc.) 
    area VARCHAR, --Área general del conocimiento 
    discipline VARCHAR, --Disciplina específica del autor 
    subdiscipline VARCHAR, --Subdisciplina del conocimiento 
    speciality VARCHAR, --Especialidad del autor dentro del área o subdisciplina 
    affilation VARCHAR, --Afiliación registrada del autor (no enlazada a tabla de afiliaciones directamente) 
    country VARCHAR, --País de la afiliación o del registro 
    state VARCHAR, --Estado donde se ubica la afiliación 
    federal_entity VARCHAR, -- Entidad federativa (solo aplica si es en México) 
    PRIMARY KEY (cvu, start_year), --Llave primaria compuesta por cvu y año de inicio 
    FOREIGN KEY (cvu) REFERENCES authorssni(cvu) --Relación con la tabla authorssni 
);

--Se crea la tabla papers_authors_affiliations
CREATE TABLE papers_authors_affiliations(
    affilation_id INT, --Identificador de la afiliación (llave foránea hacia affiliation) 
    paper_author_id INT, --Identificador del autor-paper (llave foránea hacia papers_authors) 
    FOREIGN KEY (affilation_id) REFERENCES affiliation(affilation_id), --Relación con la tabla affiliation 
    FOREIGN KEY (paper_author_id) REFERENCES papers_authors(paper_author_id) --Relación con la tabla papers_authors 
);

--Se crea la tabla authors_papers_cites
CREATE TABLE authors_papers_cites(
    author_scopus_id VARCHAR, --Identificador del autor (no está conectado como llave foránea por diseño) 
    eid VARCHAR, --Identificador del artículo científico 
    year INT, --Año en que se cuenta la citación 
    cites_count INT, --Número de citas que recibió ese paper para ese autor ese año 
    PRIMARY KEY (author_scopus_id, eid, year) --Llave primaria compuesta por autor, paper y año 
);

/*

Las siguientes tablas son las que están en morado, a pesar que no existan
decidí transcribirlas por si en algún futuro es necesario trabajarlas

CREATE TABLE funders(
    fund_no INT PRIMARY KEY,
    fund_acr VARCHAR,
    fund_sponsor VARCHAR
);

CREATE TABLE papers_funders(
    eid VARCHAR,
    fund_no INT,
    PRIMARY KEY (eid, fund_no),
    FOREIGN KEY (eid) REFERENCES papers(eid),
    FOREIGN KEY (fund_no) REFERENCES funders(fund_no)
);

CREATE TABLE subjects(
    subject_id INT PRIMARY KEY,
    subject VARCHAR
);

CREATE TABLE papers_subjects(
    eid VARCHAR,
    subject_id INT,
    PRIMARY KEY (eid, subject_id),
    FOREIGN KEY (eid) REFERENCES papers(eid),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE references(
    eid VARCHAR,
    reference_eid VARCHAR,
    position INT,
    PRIMARY KEY (eid, reference_eid),
    FOREIGN KEY (eid) REFERENCES papers(eid)
);

CREATE TABLE areas(
    area_id INT PRIMARY KEY,
    area VARCHAR
);

CREATE TABLE authors_areas(
    author_scopus_id VARCHAR,
    area_id INT,
    PRIMARY KEY (author_scopus_id, area_id),
    FOREIGN KEY (author_scopus_id) REFERENCES authors(author_scopus_id),
    FOREIGN KEY (area_id) REFERENCES areas(area_id)
);
*/


--Algunos datos de prueba

SELECT * FROM  papers_authors;

--Sources de prueba
-- Source 1
INSERT INTO sources(source_id, publication_name, issn, eissn, aggregation_type) VALUES 
	
    ('SRC100', 'Revista del Bienestar', '1234-5678', '8765-4321', 'journal'),
    ('SRC200', 'TV Churros científico', '2345-6789', '9876-5432', 'journal'),
    ('SRC300', 'Estudio Águila', '3456-7890', '4321-0987', 'conference');


--probamos la tabla
SELECT * FROM  sources;

--Se insertan autores sni de prueba (perdon si uso nombres de personajes, pero hay que
--hacer divertido el PT)
INSERT INTO authorssni(cvu, names, surnames, nobilis, init_year, career_length) VALUES
	
	('CVU101', 'Mario', 'Castañeda', NULL, 2012, 12),
	('CVU102', 'Saturo', 'Gojo', 'Dr.', 2008, 16),
	('CVU103', 'Travis', 'Scott', NULL, 2015, 9);

--probamos la tabla
SELECT * FROM  authorssni;

--Se insertan autores normales de prueba

INSERT INTO authors(author_scopus_id, cvu, author_scopus_name, 
	ORCID, cites_by_documents, cites_by_authors) VALUES
	
	('SCOPUS101', 'CVU101', 'Mario Castañeda', '0000-0001-1111-2222', 50, 20),
	('SCOPUS102', 'CVU102', 'Saturo Gojo', '0000-0002-3333-4444', 75, 30),
	('SCOPUS103', 'CVU103', 'Travis Scott', '0000-0003-5555-6666', 60, 25);

--probamos la tabla
SELECT * FROM  authors;

--metemos unos articulos de ejemplo

-- Insertar 3 artículos con fuentes válidas

INSERT INTO papers(eid, source_id, authors_ids, doi, pii, 
	pubmed, title, subtype, subtype_description, 
	author_count, year, cover_date,
    cover_display_date, volume, issue_identifier,
	article_number, page_range, description, authkeywords, 
	citedby_count, openaccess, freetoread, freetoread_label) VALUES
--Artículo 1: Mario Castañeda
		('EID001', 
		'SRC100', 
		'SCOPUS101', 
		'10.1234/abc.def', 
		'PII001', 
		'PM001',
		'Estudio sobre cómo ser parte de la mafia del doblaje', 
		'research-article', 'Artículo de investigación',
		1, 2024, 
		'2024-05-20', 
		'Mayo 2024', 
		'Vol. 1', 
		'Issue 1', 
		'Art01', 
		'10-18',
		'Un artículo que estudia los actores de doblaje', 
		'doblaje, 
		Adobe Audition, 
		arte',
		0, 
		'sí', 
		'sí', 
		'Acceso limitado'),

--Artículo 2: Satoru Gojo
		('EID002', 
		'SRC200', 
		'SCOPUS102', 
		'10.9999/infinito.gojo', 
		'PII002', 
		'PM002',
		'Dominando la energía maldita: un enfoque infinito', 
		'research-article', 
		'Artículo técnico',
		 1, 2023, 
		'2023-11-10', 
		'Noviembre 2023', 
		'Vol. 2', 
		'Issue 5', 
		'Art02', 
		'22-30',
		 'Este artículo presenta una formulación teórica y práctica del Límite Infinito como sistema de defensa absoluta en entornos de alta maldición.',
		'energía maldita, 
		Límite Infinito, 
		Seis Ojos, Gojo, 
		técnicas jujutsu',
		 5, 
		'sí', 
		'no', 
		'Acceso parcial'),

--Artículo 3: Travis Scott
		('EID003', 
		'SRC300', 
		'SCOPUS103', 
		'10.4012/conciertos.seg2022',
		'PII003', 
		'PM003',
		'Cómo prevenir accidentes en conciertos masivos: el caso Astroworld 2021 como antecedente',
		'research-article', 'Artículo académico',
		1, 
		2022, 
		'2022-08-15', 
		'Agosto 2022', 
		'Vol. 3', 
		'Issue 2', 
		'Art03', 
		'31-40',
		'Este artículo analiza los riesgos en eventos masivos a partir de la tragedia ocurrida en el festival Astroworld 2021. Se proponen estrategias preventivas, mejoras en control de multitudes, monitoreo en tiempo real y responsabilidad organizacional.',
		'seguridad en eventos, Astroworld 2021, control de multitudes, prevención de riesgos, conciertos',
		12, 
		'sí', 
		'sí', 
		'Acceso abierto');

--probamos la tabla
SELECT * FROM  papers;

--Se insertan relaciones entre artículos y autores de prueba que ya estan pero las relacionamos en la
--tablita intermedia
INSERT INTO papers_authors(paper_author_id, eid, authors_scopus_id, is_creator) VALUES
	(1, 'EID001', 'SCOPUS101', TRUE),  -- es de Mario Castañeda
	(2, 'EID002', 'SCOPUS102', TRUE),  -- es de Satoru Gojo
	(3, 'EID003', 'SCOPUS103', TRUE);  -- es de Travis Scott

--probamos la tabla intermedia
SELECT * FROM  papers_authors;

--Se insertan afiliaciones de prueba
INSERT INTO affiliation(affilation_id, affilation_name, affilation_city, affilation_country) VALUES
	(1, 'IMBAL', 'Ciudad de México', 'México'), --es de Mario Castañeda, se que es INBAL
	(2, 'Universidad Hechicera de Tokio', 'Tokio', 'Japón'), --Es de Saturo Gojo
	(3, 'Cactus Jack University', 'Houston', 'Estados Unidos'); --Es de Travis Scott

--probamos la tabla
SELECT * FROM  affiliation;

--Se insertan relaciones autor-artículo-afiliación para la tablita intermedia de prueba
INSERT INTO papers_authors_affiliations(affilation_id, paper_author_id) VALUES
	
	(1, 1),  -- Mario Castañeda
	(2, 2),  -- Satoru Gojo
	(3, 3);  -- Travis Scott

--probamos la tabla
SELECT * FROM  papers_authors_affiliations;


--Se insertan ls relaciones de autor-productividad de prueba
INSERT INTO authors_productivity(author_scopus_id, year, hindex, publications_count, cites_count) VALUES
	
	('SCOPUS101', 2024, 8, 3, 25),   -- Mario Castañeda
	('SCOPUS102', 2023, 12, 4, 40),  -- Satoru Gojo
	('SCOPUS103', 2022, 6, 2, 18);   -- Travis Scott

--probamos la tabla
SELECT * FROM  authors_productivity;

--Se insertan las relaciones de autor-productividad de prueba

INSERT INTO papers_productivity(eid, year, cites_count) VALUES
	
	('EID001', 2024, 5),   -- Artículo de Mario
	('EID002', 2023, 10),  -- Artículo de Gojo
	('EID003', 2022, 8);   -- Artículo de Travis

--probamos la tabla
SELECT * FROM  papers_productivity;

--Se insertan relaciones de autor-articulo-citas de prueba
INSERT INTO authors_papers_cites(author_scopus_id, eid, year, cites_count) VALUES
	
	('SCOPUS101', 'EID001', 2024, 5),
	('SCOPUS102', 'EID002', 2023, 10),
	('SCOPUS103', 'EID003', 2022, 8);

--probamos la tabla
SELECT * FROM  authors_papers_cites;

--Se insertan datos en fuentes-productividad de prueba

INSERT INTO sources_productivity(source_id, year, SJR, SNIP, cite_score, rank, percentile, quartile) VALUES
	
	('SRC100', 2024, '1.2', '0.9', '3.5', 'Q1', '90', 'Q1'),
	('SRC200', 2023, '1.0', '0.8', '3.0', 'Q2', '75', 'Q2'),
	('SRC300', 2022, '0.7', '0.6', '2.4', 'Q3', '60', 'Q3');

--Probamos la tabla
SELECT * FROM  sources_productivity;


--Se insertan los tipos de keywords / tipos de palabras claves de prueba
INSERT INTO keyword_types(keyword_type_id, name) VALUES
	(1, 'Temática'), 
	(2, 'Técnica'), 
	(3, 'Contextual');

--Probamos la tabla
SELECT * FROM  keyword_types;

--Se insertan palabras clave de prueba
INSERT INTO keywords(keyword_id, keyword, keyword_type_id) VALUES
	(101, 'doblaje', 1), 
	(102, 'Adobe Audition', 2), 
	(103, 'arte', 3),
	(104, 'energía maldita', 1), 
	(105, 'Gojo', 3),
	(106, 'Astroworld', 1), 
	(107, 'conciertos', 3);

--Probamos la tabla
SELECT * FROM  keywords;

--Se insertan datos de la relación con artículos y sus palabras clave de prueba
INSERT INTO papers_keywords(eid, keyword_id) VALUES
	
	('EID001', 101), 
	('EID001', 102), 
	('EID001', 103),
	('EID002', 104), 
	('EID002', 105),
	('EID003', 106), 
	('EID003', 107);

SELECT * FROM  papers_keywords;

--Ahora, haremos algunos join para probar los datos insertados
--Vamos a ver los autores y sus articulos
SELECT author.author_scopus_name author_name, paper.title article_title, paper.year publication_year
		FROM authors author
		JOIN papers_authors link ON author.author_scopus_id = link.authors_scopus_id
		JOIN papers paper ON link.eid = paper.eid;

--Ahora vamos a ver los artículos y sus palabras clave
SELECT paper.title article_title, keyword.keyword keyword_text
		FROM papers paper
		JOIN papers_keywords link ON paper.eid = link.eid
		JOIN keywords keyword ON link.keyword_id = keyword.keyword_id;

--Ahora vamos a ver los autores sus afiliaciones por artículo

SELECT author.author_scopus_name AS author_name, affiliation.affilation_name AS affiliation_name,
    	paper.title AS article_title
		FROM authors author
		JOIN papers_authors link ON author.author_scopus_id = link.authors_scopus_id
		JOIN papers paper ON link.eid = paper.eid
		JOIN papers_authors_affiliations middle ON link.paper_author_id = middle.paper_author_id
		JOIN affiliation affiliation ON middle.affilation_id = affiliation.affilation_id
		GROUP BY author.author_scopus_name, affiliation.affilation_name, paper.title
		ORDER BY author.author_scopus_name, paper.title;


--Ahora veremos la productividad del autor y sus citas por año
SELECT productivity.author_scopus_id, author.author_scopus_name author_name, productivity.year,
       productivity.cites_count total_citations
		FROM authors_productivity productivity
		JOIN authors author ON productivity.author_scopus_id = author.author_scopus_id;

--Veremos la productividad de una fuente en año
SELECT source.publication_name publication_name, productivity.year, productivity.cite_score cite_score
		FROM sources source
		JOIN sources_productivity productivity ON source.source_id = productivity.source_id;





DROP TABLE IF EXISTS
    papers_authors_affiliations,
    papers_keywords,
    papers_subjects,
    papers_funders,
    authors_areas,
    authors_papers_cites,
    authors_productivity,
    authorssni_info,
    authorssni,
    affiliation,
    papers_authors,
    papers,
    sources_productivity,
    sources,
    authors,
    funders,
    keywords,
    keyword_types,
    subjects,
    areas
CASCADE;

