DROP TABLE public.records;

CREATE TABLE public.records
(
  identifier character varying NOT NULL
  content character varying(255) NOT NULL,
  abstract text NOT NULL,
  publicationyear integer NOT NULL,
  publicationlineage character varying(255),
  geography character varying(255) NOT NULL,
  geodata_type character varying(20),
  extent box2d,
  source character varying(2083) NOT NULL,
  metadata character varying(2083) NOT NULL,
  access character varying(2083) NOT NULL,
  collection character varying(255),
  dataset character varying(255),
  service character varying(20) NOT NULL,
  crs character varying(20) NOT NULL,
  terms character varying(2083) NOT NULL,
  proved date,
  modified timestamp without time zone,
  login_name character varying(50),
  visibility character varying(20) NOT NULL,
);

CREATE INDEX record_index
  ON public.records
  USING btree
  (identifier COLLATE pg_catalog."default");
