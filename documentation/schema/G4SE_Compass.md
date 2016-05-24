# G4SE Schema

| display name                | attribute name      | data type | mandatory| default | dublin core | enumeration values                         | documentation                                                                                                                      |
|-----------------------------|-------------------- |-----------|----------|---------|-------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Id                          | identifier          | string    | true     |         | identifier  |                                            | Identifier unique within G4SE; tbd. can be e.g. PREFIX+data_provider_id                                                            |
| Title                       | content             | string    | true     |         | title       |                                            | Metadata Record title (SK: Why not attr.name 'title'?)                                                                             |
| Abstract                    | abstract            | string    | true     |         | description |                                            | Multi line record abstract                                                                                                         |
| Publication year            | publication_year    | int       | true     |         | date        |                                            | Year of initial publication                                                                                                        |
| Publication lineage         | publication_lineage | string    | false    |         |             |                                            | Comma separated publication   year lineage (passed publications)                                                                   |
| Geographical coverage       | geography           | string    | true     | Schweiz | coverage    |                                            | Official BFS (Swiss Federal Statistical Office) geographical   description. Use largest covered unit (Municipality < Canton < CH). |
| Geographical extent         | extent              | string    | false    |         |             |                                            | BBox. Must be WSG84.                                                                                                               |
| Geodata type                | geodata_type        | string    | true     |         |             | raster, vector                             | Geodatatype of original data                                                                                                       |
| Source of original data     | source              | string    | true     |         | creator     |                                            | Contract partner for original data e.g. swisstopo, Canton xy... (ev. canton dept.?)                                                |
| Additional metadata         | metadata            | URI       | true     |         | relation    |                                            | URI to pdf or fileshare with several pdfs containing aditional Metadata                                                            |
| Access to?                  | access              | URI       | true     |         |             |                                            | URI to the detailed view of the record in GeoVITe or Portal (Zugang)                                                               |
| Entry point                 | entry_point         | string    | false    |         |             |                                            | Entry point ???                                                                                                                    |
| Group                       | collection          | string    | false    |         |             |                                            | Group name or feature dataset ???                                                                                                  |
| Dataset name                | dataset             | string    | false    |         |             |                                            | Dataset (in future ev. file name)                                                                                                  |
| ArcGIS layer link           | arcgis_rest_url     | string    | false    |         |             |                                            | Weblink to a file (.pitem) hosted on a G4SE share close to metadata                                                                |
| ArcGIS symbology link       | arcgis_symbology_url| string    | false    |         |             |                                            | Weblink to a file (.lyr) hosted on a G4SE share close to metadata                                                                  |
| QGIS symbology link         | qgis_symbology_url  | string    | false    |         |             |                                            | Weblink to a file (.sld) hosted on a G4SE share close to metadata                                                                  |
| Service type                | service_type        | string    | false    |         | format      | WMS,WFS,GeoVite,FeatureService,ImageService| Service type (KES: more ArcGIS Services missing?)                                                                                  |
| Coordinate reference system | crs                 | string    | true     |         |             | LV03, LV95, WGS84                          | CRS of original data (EPSG)                                                                                                        |
| Terms of use                | terms               | URI       | true     |         | rights      |                                            | URI to PDF with information about the terms of use                                                                                 |
| Proving date                | proved              | date      | false    |         |             |                                            | Most recent proving date                                                                                                           |
| Last modification           | modified            | datetime  | false    | (system)|             |                                            | Most recent modification time                                                                                                      |
| Login name                  | login_name          | string    | false    | (system)| contributor |                                            | Metadata Author name                                                                                                               |
| Access restriction          | visibility          | string    | true     | public  |             | public, test, hsr-internal                 | Metadata visibility in front end                                                                                                   |

# Data access
Currently dataset and collection define data access/source (accompanied with mandatory service_type). This is still unclear...!

Data sources:
* ArcGIS REST Services (Kompatibel mit QGIS nur mittels Connector Plugin), z.B. dataset="pixelkarte100", collection="https://geodata4edu.hsr.ch/geodata/rest/services/Basisdaten/" (siehe https://geodata4edu.hsr.ch/geodata/rest/services/Basisdaten/pixelkarte100/ImageServer , title pixelkarte100  (Quelle: http://wiki.hsr.ch/StefanKeller/wiki.cgi?WikiSandbox))
* GeoVITE, ???
* Weitere (nicht geplant):
** ArcGIS REST Services (Kompatibel mit QGIS mittels Plugin), z.B. dataset="FUSSGAENGERSTREIFEN_P", collection="" (siehe http://maps.hsr.ch/gdi/rest/services/KTZH/FUSSGAENGERSTREIFEN_P/MapServer/0 , Basis-URL: http://maps.hsr.ch/gdi/rest/services/ )
** Daten File auf Share (Kompatibel mit QGIS), z.B. http://geodatenkompass.hsr.ch/gdishare/osm.zip 
** ArcGIS-Datenbank (à la Geodatenkompass HSR) (Kompatibel mit QGIS), z.B. mit Geodaten="db_ktzh",  Collection="NaturUndLandschaft", Class="LICHTE_WAELDER" (siehe Metadaten-Weblink http://geodatenkompass.hsr.ch/#id=20700)

# Mapping to Dublin core

Unclear Dublin core fields with descrtiption from the DC documentation (http://dublincore.org/documents/dces/)
* subject - "Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary.""
* source - "The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system."
* type - "Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the Format element."

Fields that are not in the G4SE Schema: language (= german for data content?)

See also: DCAP Application Profile Spec.: http://dublincore.org/groups/collections/collection-application-profile/
