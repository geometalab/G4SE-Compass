DROP TABLE public.records;

CREATE TABLE public.records
(
  identifier character varying NOT NULL,
  language character varying(20) NOT NULL,
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  keywords_en character varying(255) NOT NULL,
  keywords_de character varying(255) NOT NULL,
  keywords_fr character varying(255) NOT NULL,
  publicationyear integer NOT NULL,
  publicationlineage character varying(255),
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
);

CREATE INDEX record_index
  ON public.records
  USING btree
  (identifier COLLATE pg_catalog."default");
