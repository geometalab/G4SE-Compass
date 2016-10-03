export class Metadata {
  api_id: string;
  content: string;
  identifier: string;
  language: string; // de, fr, en
  abstract: string;
  publication_year: string; // should change to number soonish
  publication_lineage: string; // array would be better, but...
  geography: string;
  extent: string; // should change to geoJSON someday
  geodata_type: string;
  source: string;
  metadata_link: string; // URL
  access_link: string; // URL
  base_link: string; // URL
  collection: string;
  dataset: string;
  arcgis_layer_link: string; // URL
  qgis_layer_link: string; // URL
  arcgis_symbology_link: string; // URL
  qgis_symbology_link: string; // URL
  service_type: string;
  crs:  string; // in the form of "EPSG:4326"
  term_link: string; // URL
  proved: string;
  visibility:  string; // URL
  modified:  string; // URL
}
