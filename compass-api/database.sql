CREATE EXTENSION IF NOT EXISTS postgis
    SCHEMA public
    VERSION "2.2.2";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create table for internally organized records
CREATE TABLE IF NOT EXISTS public.records
(
  api_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY ,
  identifier character varying NOT NULL,
  language character varying(20) NOT NULL,
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  publication_year character varying(20) NOT NULL,
  publication_lineage character varying(255),
  geography character varying(255) NOT NULL,
  extent box2d,
  geodata_type character varying(255) NOT NULL,
  source character varying(2083) NOT NULL,
  metadata_link character varying(2083) NOT NULL,
  access_link character varying(2083) NOT NULL,
  base_link character varying(2083),
  collection character varying(255),
  dataset character varying(255),
  arcgis_layer_link character varying(2083),
  qgis_layer_link character varying(2083),
  arcgis_symbology_link character varying(2083),
  qgis_symbology_link character varying(2083),
  service_type character varying(255),
  crs character varying(20) NOT NULL,
  term_link character varying(2083) NOT NULL,
  proved date,
  visibility character varying(255) NOT NULL,
  modified timestamp without time zone,
  login_name character varying(255),
  search_vector_de tsvector,
  search_vector_en tsvector,
  search_vector_fr tsvector
)
WITH (
  OIDS=FALSE
);

-- Create table for harvested records
CREATE TABLE IF NOT EXISTS public.harvested_records
(
  api_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
  identifier character varying NOT NULL,
  language character varying(20) NOT NULL,
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  publication_year character varying(20) NOT NULL,
  publication_lineage character varying(255),
  geography character varying(255) NOT NULL,
  extent box2d,
  geodata_type character varying(255) NOT NULL,
  source character varying(2083) NOT NULL,
  metadata_link character varying(2083) NOT NULL,
  access_link character varying(2083) NOT NULL,
  base_link character varying(2083),
  collection character varying(255),
  dataset character varying(255),
  arcgis_layer_link character varying(2083),
  qgis_layer_link character varying(2083),
  arcgis_symbology_link character varying(2083),
  qgis_symbology_link character varying(2083),
  service_type character varying(255),
  crs character varying(20) NOT NULL,
  term_link character varying(2083) NOT NULL,
  proved date,
  visibility character varying(255) NOT NULL,
  modified timestamp without time zone,
  login_name character varying(255),
  search_vector_de tsvector,
  search_vector_en tsvector,
  search_vector_fr tsvector
)
WITH (
  OIDS=FALSE
);


-- Create view that returns the contents of all record tables, extent must be casted to text for the query to work
CREATE OR REPLACE VIEW public.all_records AS 
 SELECT
    records.extent::text,
    records.api_id,
    records.identifier,
    records.language,
    records.content,
    records.abstract,
    records.publication_year,
    records.publication_lineage,
    records.geography,
    records.geodata_type,
    records.source,
    records.metadata_link,
    records.access_link,
    records.base_link,
    records.collection,
    records.dataset,
    records.arcgis_layer_link,
    records.qgis_layer_link,
    records.arcgis_symbology_link,
    records.qgis_symbology_link,
    records.service_type,
    records.crs,
    records.term_link,
    records.proved,
    records.visibility,
    records.modified,
    records.login_name,
    records.search_vector_de,
    records.search_vector_en,
    records.search_vector_fr
   FROM records
UNION
 SELECT
    harvested_records.extent::text,
    harvested_records.api_id,
    harvested_records.identifier,
    harvested_records.language,
    harvested_records.content,
    harvested_records.abstract,
    harvested_records.publication_year,
    harvested_records.publication_lineage,
    harvested_records.geography,
    harvested_records.geodata_type,
    harvested_records.source,
    harvested_records.metadata_link,
    harvested_records.access_link,
    harvested_records.base_link,
    harvested_records.collection,
    harvested_records.dataset,
    harvested_records.arcgis_layer_link,
    harvested_records.qgis_layer_link,
    harvested_records.arcgis_symbology_link,
    harvested_records.qgis_symbology_link,
    harvested_records.service_type,
    harvested_records.crs,
    harvested_records.term_link,
    harvested_records.proved,
    harvested_records.visibility,
    harvested_records.modified,
    harvested_records.login_name,
    harvested_records.search_vector_de,
    harvested_records.search_vector_en,
    harvested_records.search_vector_fr
   FROM harvested_records;


-- Search vector triggers for internal metadata records
CREATE OR REPLACE FUNCTION records_trigger_de()RETURNS trigger AS $$
begin
  new.search_vector_de :=
    setweight(to_tsvector('pg_catalog.german', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER tsvectorupdate_de BEFORE INSERT OR UPDATE
    ON records FOR EACH ROW EXECUTE PROCEDURE records_trigger_de();


CREATE OR REPLACE FUNCTION records_trigger_en()RETURNS trigger AS $$
begin
  new.search_vector_en :=
    setweight(to_tsvector('pg_catalog.german', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER tsvectorupdate_en BEFORE INSERT OR UPDATE
    ON records FOR EACH ROW EXECUTE PROCEDURE records_trigger_en();


CREATE OR REPLACE FUNCTION records_trigger_fr()RETURNS trigger AS $$
begin
  new.search_vector_fr :=
    setweight(to_tsvector('pg_catalog.german', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER tsvectorupdate_fr BEFORE INSERT OR UPDATE
    ON records FOR EACH ROW EXECUTE PROCEDURE records_trigger_fr();


-- Search vector triggers for harvested metadata records
CREATE OR REPLACE FUNCTION harvested_records_trigger_de()RETURNS trigger AS $$
begin
  new.search_vector_de :=
    setweight(to_tsvector('pg_catalog.german', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.german', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER harvested_tsvectorupdate_de BEFORE INSERT OR UPDATE
    ON harvested_records FOR EACH ROW EXECUTE PROCEDURE harvested_records_trigger_de();


CREATE OR REPLACE FUNCTION harvested_records_trigger_en()RETURNS trigger AS $$
begin
  new.search_vector_en :=
    setweight(to_tsvector('pg_catalog.english', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.english', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.english', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.english', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.english', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER harvested_tsvectorupdate_en BEFORE INSERT OR UPDATE
    ON harvested_records FOR EACH ROW EXECUTE PROCEDURE harvested_records_trigger_en();


CREATE OR REPLACE FUNCTION harvested_records_trigger_fr()RETURNS trigger AS $$
begin
  new.search_vector_fr :=
    setweight(to_tsvector('pg_catalog.french', coalesce(new.content,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.french', coalesce(new.abstract,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.french', coalesce(new.geography,'')), 'A') ||
    setweight(to_tsvector('pg_catalog.french', coalesce(new.collection,'')), 'B') ||
    setweight(to_tsvector('pg_catalog.french', coalesce(new.dataset,'')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER harvested_tsvectorupdate_fr BEFORE INSERT OR UPDATE
    ON harvested_records FOR EACH ROW EXECUTE PROCEDURE harvested_records_trigger_fr();

