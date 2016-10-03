export class SearchResult {
  api_id: string;
  text: string;
  content: string;
  language: string; // de, fr, en
  abstract: string;
  publication_year: string; // should change to number soonish
  geography: string;
  source: string;
  collection: string;
  dataset: string;
  service_type: string;
  crs:  string; // in the form of "EPSG:4326"
  visibility:  string; // URL
  modified:  string; // URL
  highlighted: string; // HTML
}
