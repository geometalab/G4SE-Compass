# G4SE Schema

| display name                | attribute name       | data type | mand.| default | dublin core | enumeration values               | documentation                                                                                                                      |
|-----------------------------|----------------------|-----------|------|---------|-------------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Id                          | identifier           | string    | yes  |         | identifier  |                                  | Identifier unique within G4SE; tbd. can be e.g. PREFIX+data_provider_id                                                            |
| Title                       | content              | string    | yes  |         | title       |                                  | Metadata Record title (SK: Why not attr.name 'title'?)                                                                             |
| Abstract                    | abstract             | string    | yes  |         | description |                                  | Multi line record abstract                                                                                                         |
| Publication year            | publication_year     | int       | yes  |         | date        |                                  | Year of initial publication                                                                                                        |
| Publication lineage         | publication_lineage  | string    | no   |         |             |                                  | Comma separated publication   year lineage (passed publications)                                                                   |
| Geographical coverage       | geography            | string    | yes  |(Schweiz)| coverage    |                                  | Official BFS (Swiss Federal Statistical Office) geographical description. Use largest covered unit (Municipality < Canton < CH). |
| Geographical extent         | extent               | string    | no   |         |             |                                  | BBox. Must be WSG84.                                                                                                               |
| Geodata type                | geodata_type         | string    | yes  |         |             | raster,vector,other              | Geodatatype of original data                                                                                                       |
| Source of original data     | source               | string    | yes  |         | creator     |                                  | Contract partner for original data e.g. swisstopo, Canton xy... (ev. canton dept.?)                                                |
| Additional metadata         | metadata_link        | URL       | yes  |         | relation    |                                  | URI to pdf or fileshare with several pdfs containing aditional Metadata                                                            |
| Access to data              | access_link          | URL       | yes  |         |             |                                  | URI to the detailed view of the record in GeoVITe or Portal (Zugang)                                                               |
| Entry point                 | entry_point          | string    | no   |         |             |                                  | Entry point ???                                                                                                                    |
| Group                       | collection           | string    | no   |         |             |                                  | Group name or feature dataset ???                                                                                                  |
| Dataset name                | dataset              | string    | no   |         |             |                                  | Dataset (in future ev. file name)                                                                                                  |
| ArcGIS layer link           | arcgis_rest_link     | URL       | no   |         |             |                                  | Weblink to a file (.pitem) hosted on a G4SE share close to metadata                                                                |
| ArcGIS symbology link       | arcgis_symbology_link| URL       | no   |         |             |                                  | Weblink to a file (.lyr) hosted on a G4SE share close to metadata                                                                  |
| QGIS symbology link         | qgis_symbology_link  | URL       | no   |         |             |                                  | Weblink to a file (.sld) hosted on a G4SE share close to metadata                                                                  |
| Service type                | service_type         | string    | no   |         | format      | WMS,WFS,GeoVITe,Feature,Image,???| Service type (KES: more ArcGIS Services missing?)                                                                                  |
| Coordinate reference system | crs                  | string    | yes  |         |             | LV03,LV95,WGS84,other            | CRS of original data (EPSG)                                                                                                        |
| Terms of use                | term_link            | URL       | yes  |         | rights      |                                  | URI to PDF with information about the terms of use                                                                                 |
| Proving date                | proved               | date      | no   |         |             |                                  | Most recent proving date                                                                                                           |
| Access restriction          | visibility           | string    | yes  | public  |             | public,test,hsr-internal         | Metadata visibility in front end                                                                                                   |
| Last modification           | modified             | datetime  | no   | (system)|             |                                  | Most recent modification time                                                                                                      |
| Login name                  | login_name           | string    | no   | (system)| contributor |                                  | Metadata Author name                                                                                                               |

# Data access
Currently dataset and collection define data access/source (accompanied with mandatory service_type). This is still unclear...!

Data sources:
* ArcGIS REST Services (Kompatibel mit QGIS nur mittels Connector Plugin), z.B. dataset="pixelkarte100", collection="https://geodata4edu.hsr.ch/geodata/rest/services/Basisdaten/" (siehe https://geodata4edu.hsr.ch/geodata/rest/services/Basisdaten/pixelkarte100/ImageServer , title pixelkarte100  (Quelle: http://wiki.hsr.ch/StefanKeller/wiki.cgi?WikiSandbox))
* GeoVITE, tbd.
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
