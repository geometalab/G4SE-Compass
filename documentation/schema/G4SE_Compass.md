# G4SE Schema
 
| display name (de)             | display name (en)           | attribute name        | data type | mand. | default  | dublin core |OAI| enumeration values                        | documentation                                                                                                                    |                                            | 
|-------------------------------|-----------------------------|-----------------------|-----------|-------|----------|-------------|---|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| (Identifikator)               | (Id)                        | identifier            | string    | yes   |          | identifier  | x |                                           | "Identifier unique within G4SE                                                                                                   |  tbd. can be e.g. PREFIX+data_provider_id" | 
| Titel                         | Title                       | content               | string    | yes   |          | title       | x |                                           | Metadata Record title (SK: Why not attr.name 'title'?)                                                                           |                                            | 
| Beschreibung                  | Abstract                    | abstract              | string    | yes   |          | description | x |                                           | Multi line record abstract                                                                                                       |                                            | 
| Zeit                          | Publication year            | publication_year      | int       | yes   |          | date        | x |                                           | Year of initial publication                                                                                                      |                                            | 
| History                       | Publication lineage         | publication_lineage   | string    | no    |          |             | x |                                           | Comma separated publication   year lineage (passed publications), ascending                                                   |                                            | 
| Geogr. Bezugsname             | Geographical coverage       | geography             | string    | yes   | (Schweiz)| coverage    | x |                                           | Official BFS (Swiss Federal Statistical Office) geographical description. Use largest covered unit (Municipality < Canton < CH). |                                            | 
| Geogr. Ausdehnung             | Geographical extent         | extent                | string    | no    |          |             | x |                                           | Box WKT (2D). Must be WSG84.                                                                                                             |                                            | 
| Geodatentyp                   | Geodata type                | geodata_type          | string    | yes   |          |             | x | raster,vector,other                       | Geodatatype of original data                                                                                                     |                                            | 
| Bezugsquelle                  | Source of original data     | source                | string    | yes   |          | creator     | x |                                           | Contract partner for original data e.g. swisstopo, Canton xy... (ev. canton dept.?)                                              |                                            | 
| Metadaten                     | Additional metadata         | metadata_link         | URL       | yes   |          | relation    | x |                                           | URI to pdf or fileshare with several pdfs containing aditional Metadata                                                          |                                            | 
| Zugang                        | Access to data              | access_link           | URL       | yes   |          |             | x |                                           | URI to the detailed view of the record in GeoVITe or Portal (Zugang)                                                             |                                            | 
| Basis URL                     | Entry point                 | base_link             | string    | no    |          |             | x |                                           | Entry point ???                                                                                                                  |                                            | 
| Gruppe                        | Group                       | collection            | string    | no    |          |             |   |                                           | Group name or feature dataset ???                                                                                                |                                            | 
| Datensatz-Name                | Dataset name                | dataset               | string    | no    |          |             |   |                                           | Dataset (in future ev. file name)                                                                                                |                                            | 
| ArcGIS layer link             | ArcGIS layer link           | arcgis_layer_link     | URL       | no    |          |             |   |                                           | Weblink to a file (.pitem) hosted on a G4SE share close to metadata                                                              |                                            | 
| QGIS layer link               | QGIS layer link             | qgis_layer_link       | URL       | no    |          |             |   |                                           |                                                                                                                                  |                                            | 
| ArcGIS symbology link         | ArcGIS symbology link       | arcgis_symbology_link | URL       | no    |          |             |   |                                           | Weblink to a file (.lyr) hosted on a G4SE share close to metadata                                                                |                                            | 
| QGIS symbology link           | QGIS symbology link         | qgis_symbology_link   | URL       | no    |          |             |   |                                           | Weblink to a file (.sld) hosted on a G4SE share close to metadata                                                                |                                            | 
| Service-Art                   | Service type                | service_type          | string    | no    |          | format      | x | FeatureService,MapService,GeoVITe,WMS,WFS | Service type (KES: more ArcGIS Services missing?)                                                                                |                                            | 
| Koordinatensystem             | Coordinate reference system | crs                   | string    | yes   |          |             | x | LV03,LV95,WGS84,other                     | CRS of original data (EPSG)                                                                                                      |                                            | 
| Nutzungsbedingungen           | Terms of use                | term_link             | URL       | yes   |          | rights      | x |                                           | URI to PDF with information about the terms of use                                                                               |                                            | 
| Letzte Aktualitätsprüfung     | Proving date                | proved                | date      | no    |          |             | x |                                           | Most recent proving date                                                                                                         |                                            | 
| Zugriffseinschränkungen       | Access restriction          | visibility            | string    | yes   | public   |             | x | public,test,hsr-internal                  | Metadata visibility in front end                                                                                                 |                                            | 
| Letzte Bearbeitung            | Last modification           | modified              | datetime  | no    | (system) |             | - |                                           | Most recent modification time                                                                                                    |                                            | 
| Loginname Bearbeiter          | Login name                  | login_name            | string    | no    | (system) | contributor | - |                                           | Metadata Author name                                                                                                             |                                            | 


# Data access
Currently dataset and collection define data access/source (accompanied with mandatory service_type). This is still unclear...!

# Data sources
## GeoVITe - Webapp:
* Weblink
 
## ArcGIS REST API FeatureService:
* ArcGIS (mit Direct Access Link)
* ArcGIS (mit Entry Point)
* QGIS Connector v0.x (mit Direct Access Link)
* QGIS Connector v1.x geplant (mit Entry Point)
 
## ArcGIS REST API MapService (new):
* QGIS QuickMapService Plugin (mit gdal_ags.xml)
 
## WMS (nice-to-have): 
* QGIS Core (mit Entry point URL) 
* QGIS QuickMapService Plugin (mit Entry point)
 
## Examples
### GeoVITe:
* Access to data        : http://geodata4edu.ethz.ch/portal.jsp?layer=P3_swissimage25cm_swissimage&timestamp=Latest&topic=25cm
* ArcGIS layer link     : -
* QGIS layer link       : -
* Entry point           : http://geodata4edu.ethz.ch/
* Group                 : -
* Dataset name          : -
* Service type          : GeoVITe
* ArcGIS symbology link : 
* QGIS symbology link   : 
 
 
### ArcGIS REST API FeatureService:
* Access to data        : https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_FLIESSGEWAESSER/FeatureServer  
* ArcGIS layer link     : https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER.pitem
* QGIS layer link       : -
* Entry point           : https://geodata4edu.hsr.ch/geodata
* Group                 : /swissTLM3D/
* Dataset name          : TLM_FLIESSGEWAESSER
* Service type          : FeatureService
* ArcGIS symbology link : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.lyr
* QGIS symbology link   : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.sld
                
### ArcGIS REST API MapService:
* Access to data        : https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_BODENBEDECKUNG/MapServer  
* ArcGIS layer link     : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.pitem
* QGIS layer link       : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.xml
* Entry point           : https://geodata4edu.hsr.ch/geodata
* Group                 : /swissTLM3D/
* Dataset name          : TLM_BODENBEDECKUNG
* Service type          : MapService
* ArcGIS symbology link : - 
* QGIS symbology link   : -
 
### WMS KtZH:
* Access to data        : http://wms.zh.ch/TbaBaustellenZHWMS
* ArcGIS layer link     : -
* QGIS layer link       : -
* Entry point           : http://wms.zh.ch/
* Group                 : TbaBaustellenZHWMS/
* Dataset name          : baustellen-detailansicht
* Service type          : WMS
* ArcGIS symbology link : 
* QGIS symbology link   : 



# Mapping to Dublin core

Unclear Dublin core fields with descrtiption from the DC documentation (http://dublincore.org/documents/dces/)
* subject - "Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary.""
* source - "The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system."
* type - "Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the Format element."

Fields that are not in the G4SE Schema: language (= german for data content?)

See also: DCAP Application Profile Spec.: http://dublincore.org/groups/collections/collection-application-profile/
