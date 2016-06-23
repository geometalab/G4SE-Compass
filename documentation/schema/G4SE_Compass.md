# G4SE Schema
 
| display name (de)             | display name (en)           | attribute name        | data type | mand. | default  | dublin core |OAI| enumeration values                        | documentation                                                                                                                    |                                            | 
|-------------------------------|-----------------------------|-----------------------|-----------|-------|----------|-------------|---|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| (Identifikator)               | (Id)                        | identifier            | string    | yes   |          | identifier  | x |                                           | Identifier unique within G4SE                                                                                                    |  tbd. can be e.g. PREFIX+data_provider_id" | 
| Metadaten Sprache             | Metadata language           | language              | string    | yes   |          | language    | x |                                           | Language of metadata record                                                                                                      |                                            |
| Titel                         | Title                       | content               | string    | yes   |          | title       | x |                                           | Metadata Record title (SK: Why not attr.name 'title'?)                                                                           |                                            | 
| Beschreibung                  | Abstract                    | abstract              | string    | yes   |          | description | x |                                           | Multi line record abstract                                                                                                       |                                            | 
| Zeit                          | Publication year            | publication_year      | int       | yes   |          | date        | x |                                           | Year of initial publication                                                                                                      |                                            | 
| History                       | Publication lineage         | publication_lineage   | string    | no    |          |             | x |                                           | Comma separated publication   year lineage (passed publications), ascending                                                      |                                            | 
| Geogr. Bezugsname             | Geographical coverage       | geography             | string    | yes   | (Schweiz)| coverage    | x |                                           | Official BFS (Swiss Federal Statistical Office) geographical description. Use largest covered unit (Municipality < Canton < CH). |                                            | 
| Geogr. Ausdehnung             | Geographical extent         | extent                | string    | no    |          |             | x |                                           | Box WKT (2D). Must be WSG84.                                                                                                     |                                            | 
| Geodatentyp                   | Geodata type                | geodata_type          | string    | yes   |          |             | x | raster,vector,other                       | Geodatatype of original data                                                                                                     |                                            | 
| Bezugsquelle                  | Source of original data     | source                | string    | yes   |          | creator     | x |                                           | Contract partner for original data e.g. swisstopo, Canton xy... (ev. canton dept.?)                                              |                                            | 
| Metadaten                     | Additional metadata         | metadata_link         | URL       | yes   |          | relation    | x |                                           | URI to pdf or fileshare with several pdfs containing aditional Metadata                                                          |                                            | 
| Zugang                        | Access to data              | access_link           | URL       | yes   |          |             | x |                                           | URI to the detailed view of the record in GeoVITe or Portal (Zugang)                                                             |                                            | 
| Basis URL                     | Entry point                 | base_link             | string    | no    |          |             | x |                                           | Entry point ???                                                                                                                  |                                            | 
| Gruppe                        | Group                       | collection            | string    | no    |          |             |   |                                           | Group name or feature dataset ???                                                                                                |                                            | 
| Datensatz-Name                | Dataset name                | dataset               | string    | no    |          |             |   |                                           | Dataset (in future ev. file name)                                                                                                |                                            | 
| ArcGIS layer link             | ArcGIS layer link           | arcgis_layer_link     | URL       | no    |          |             |   |                                           | Weblink to a file (.pitem), opens a layer in ArcGIS, hosted on a G4SE share close to metadata                                    |                                            | 
| QGIS layer link               | QGIS layer link             | qgis_layer_link       | URL       | no    |          |             |   |                                           | Weblink to a file (.pitem), opens a layer in QGIS, hosted on a G4SE share close to metadata                                      |                                            | 
| ArcGIS symbology link         | ArcGIS symbology link       | arcgis_symbology_link | URL       | no    |          |             |   |                                           | Weblink to a ArcGIS symbology file (.lyr) hosted on a G4SE share close to metadata                                               |                                            | 
| QGIS symbology link           | QGIS symbology link         | qgis_symbology_link   | URL       | no    |          |             |   |                                           | Weblink to a QGIS symbology file (.sld) hosted on a G4SE share close to metadata                                                 |                                            | 
| Service-Art                   | Service type                | service_type          | string    | no    |          | format      | x | FeatureService,MapService,GeoVITe,WMS,WFS | Service type (KES: more ArcGIS Services missing?)                                                                                |                                            | 
| Koordinatensystem             | Coordinate reference system | crs                   | string    | yes   |          |             | x | LV03,LV95,WGS84,other                     | CRS of original data (EPSG)                                                                                                      |                                            | 
| Nutzungsbedingungen           | Terms of use                | term_link             | URL       | yes   |          | rights      | x |                                           | URI to PDF with information about the terms of use                                                                               |                                            | 
| Letzte Aktualitätsprüfung     | Proving date                | proved                | date      | no    |          |             | x |                                           | Most recent proving (XML Date, ISO 8601) date                                                                                                         |                                            | 
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
* Metadata language         : de
* Title                     : Orthophoto
* Abstract                  : Das Orthophotomosaik SWISSIMAGE ist eine Zusammensetzung digitaler Farbluftbilder. Ein Orthophoto ist ein Luftbild bei dem die Neigungseinflüsse der Kamera und des Geländes korrigiert wurden. SWISSIMAGE bietet somit einen einheitlichen Massstab und eine einheitliche Radiometrie über die Gesamtheit der Schweiz an. Verschiedene Auflösungen (Grösse vom Pixel am Boden), von 25 cm bis 250 cm, stehen im Bereich der Schweiz und dem Fürstentum Liechtenstein zur Verfügung.
* Publication year          : 1998
* Publication lineage       : 2010, 2006, 2003, 2001, 1998
* Geographical coverage     : Schweiz
* Geographical extent       : BOX(5.9335 45.7785, 10.6891 47.839)
* Geodata type              : raster
* Source of original data   : Swisstopo
* Additional metadata       : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/landscape/swissTLM3D.parsysrelated1.47641.downloadList.97108.DownloadFile.tmp/201603swisstlm3d14okd.pdf
* Access to data            : http://geodata4edu.ethz.ch/portal.jsp?layer=P3_swissimage25cm_swissimage&timestamp=Latest&topic=25cm
* Entry point               : http://geodata4edu.ethz.ch/
* Group                     : -
* Dataset name              : P3_swissimage25cm
* ArcGIS layer link         : -
* QGIS layer link           : -
* ArcGIS symbology link     : -
* QGIS symbology link       : -
* Service type              : GeoVITe
* crs                       : EPSG:21781
* Terms of use              : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/swisstopo/legal_bases/copyright.html
* Proving date              : 2016-01-02
* Access restriction        : public
 
### ArcGIS REST API FeatureService:
* Metadata language         : de
* Title                     : Topologisches Landschaftsmodell TLM, Fliessgewässer
* Abstract                  : swissTLM3D ist das grossmassstäbliche Topografische Landschaftsmodell der Schweiz. Es umfasst die natürlichen und künstlichen Objekte wie auch die Namendaten in vektorieller Form. Mit einer hohen Genauigkeit und dem Einbezug der dritten Dimension ist swissTLM3D der genaueste und umfassendste 3D-Vektordatensatz der Schweiz. In dieser Feature Class werden die Fliessgewässer in linearer Form geführt. Die Linien sind in Richtung des Gewässerflusses gerichtet.
* Publication year          : 2012
* Publication lineage       : 2015, 2014, 2012
* Geographical coverage     : Schweiz
* Geographical extent       : BOX(5.9335 45.7785, 10.6891 47.839)
* Geodata type              : vector
* Source of original data   : Swisstopo
* Additional metadata       : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/landscape/swissTLM3D.parsysrelated1.47641.downloadList.97108.DownloadFile.tmp/201603swisstlm3d14okd.pdf
* Access to data            : https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_FLIESSGEWAESSER/FeatureServer
* Entry point               : https://geodata4edu.hsr.ch/geodata
* Group                     : /swissTLM3D/
* Dataset name              : TLM_FLIESSGEWAESSER
* ArcGIS layer link         : https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER.pitem
* QGIS layer link           : -
* ArcGIS symbology link     : https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER.lyr
* QGIS symbology link       : https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER_QGIS.zip
* Service type              : FeatureService
* CRS                       : EPSG:21781
* Terms of use              : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/swisstopo/legal_bases/copyright.html
* Proving date              : 2015-03-04
* Access restriction        : public
        
### ArcGIS REST API MapService:
* Metadata language         : de
* Title                     : Topologisches Landschaftsmodell TLM, Bodenbedeckung
* Abstract                  : swissTLM3D ist das grossmassstäbliche Topografische Landschaftsmodell der Schweiz. Es umfasst die natürlichen und künstlichen Objekte wie auch die Namendaten in vektorieller Form. Mit einer hohen Genauigkeit und dem Einbezug der dritten Dimension ist swissTLM3D der genaueste und umfassendste 3D-Vektordatensatz der Schweiz. In dieser Feature Class werden die Fliessgewässer in linearer Form geführt. Die Linien sind in Richtung des Gewässerflusses gerichtet.
* Publication year          : 2012
* Publication lineage       : 2015, 2014, 2012
* Geographical coverage     : Schweiz
* Geographical extent       : BOX(5.9335 45.7785, 10.6891 47.839)
* Geodata type              : vector
* Source of original data   : Swisstopo
* Additional metadata       : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/landscape/swissTLM3D.parsysrelated1.47641.downloadList.97108.DownloadFile.tmp/201603swisstlm3d14okd.pdf
* Access to data            : https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_BODENBEDECKUNG/MapServer  
* Entry point               : https://geodata4edu.hsr.ch/geodata
* Group                     : /swissTLM3D/
* Dataset name              : TLM_BODENBEDECKUNG
* ArcGIS layer link         : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.pitem
* QGIS layer link           : https://geodata4edu.hsr.ch/share/TLM_BODENBEDECKUNG.xml
* ArcGIS symbology link     : - 
* QGIS symbology link       : -
* Service type              : MapService
* CRS                       : EPSG:21781
* Terms of use              : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/swisstopo/legal_bases/copyright.html
* Proving date              : 2015-03-04
* Access restriction        : public
 
### WMS KtZH:
* Metadata language         : de
* Title                     : Baustellen Kantonsstrassen
* Abstract                  : Tagesaktuelle Baustellen auf dem Kantonsstrassennetz. Die vier Unterhaltregionen des Tiefbauamtes aktualisieren laufend die Informationen über bestehende und zukünftige Baustellen. Die Kommunikationsabteilung der Baudirektion des Kantons Zürich ist Ansprechpartner bei Fragen zu den Baustellen (http://www.bd.zh.ch/internet/baudirektion/de/service/nav/service/medien.html).
* Publication year          : 2005
* Publication lineage       : 2015, 2014, 2012, 2005
* Geographical coverage     : Zürich
* Geographical extent       : BOX(8.3469 47.0711, 9.0033 47.7047)
* Geodata type              : vector
* Source of original data   : Kanton Zürich
* Additional metadata       : http://www.geolion.zh.ch/geodatensatz/show?nbid=1724
* Access to data            : http://wms.zh.ch/TbaBaustellenZHWMS
* Entry point               : http://wms.zh.ch/
* Group                     : TbaBaustellenZHWMS/
* Dataset name              : baustellen-detailansicht
* ArcGIS layer link         : -
* QGIS layer link           : -
* ArcGIS symbology link     : http://www.geolion.zh.ch/geodatensatz/generatePDF?nbid=1724
* QGIS symbology link       : -
* Service type              : WMS
* CRS                       : EPSG:21781
* Terms of use              : http://www.swisstopo.admin.ch/internet/swisstopo/de/home/swisstopo/legal_bases/copyright.html
* Proving date              : 2015-08-24
* Access restriction        : public



# Mapping to Dublin core

Unclear Dublin core fields with descrtiption from the DC documentation (http://dublincore.org/documents/dces/)
* subject - "Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary.""
* source - "The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system."
* type - "Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the Format element."

Fields that are not in the G4SE Schema: language (= german for data content?)

See also: DCAP Application Profile Spec.: http://dublincore.org/groups/collections/collection-application-profile/
