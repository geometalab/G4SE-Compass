CREATE EXTENSION IF NOT EXISTS postgis
    SCHEMA public
    VERSION "2.2.2";

-- Create shared sequence for creating unique ids
CREATE SEQUENCE record_id_seq;

-- Create table for internally organized records
CREATE TABLE IF NOT EXISTS public.records
(
  api_id INT DEFAULT nextval('record_id_seq') NOT NULL PRIMARY KEY,
  identifier character varying NOT NULL,
  language character varying(20) NOT NULL,
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  publication_year integer NOT NULL,
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
  login_name character varying(255)
)
WITH (
  OIDS=FALSE
);

-- Create table for harvested records
CREATE TABLE IF NOT EXISTS public.harvested_records
(
  api_id INT DEFAULT nextval('record_id_seq') NOT NULL PRIMARY KEY,
  identifier character varying NOT NULL,
  language character varying(20) NOT NULL,
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  publication_year integer NOT NULL,
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
  login_name character varying(255)
)
WITH (
  OIDS=FALSE
);


-- Create view that returns the contents of all record tables, extent must be casted to text for the query to work
CREATE OR REPLACE VIEW public.all_records AS 
 SELECT
    st_astext(records.extent::geometry) AS extent,
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
    records.login_name
   FROM records
UNION
 SELECT
    st_astext(harvested_records.extent::geometry) AS extent,
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
    harvested_records.login_name
   FROM harvested_records;


