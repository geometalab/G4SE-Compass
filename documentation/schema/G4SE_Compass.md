|    Name                  |    Type        |    Description                                                                                                                           |
|--------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------|
|    identifier            |    string      |    Unique identifier                                                                                                                     |
|    content               |    string      |    Metadata Record title                                                                                                                 |
|    abstract              |    string      |    Multi line record abstract                                                                                                            |
|    publicationyear       |    int         |    Year of initial publication                                                                                                           |
|    publicationlineage    |    string      |    Comma separated publication year lineage (passed publications)                                                                        |
|    geography             |    string      |    Official BFS (Swiss Federal Statistical Office) geographical   description. Use largest covered unit (Municipality < Canton < CH).    |
|    extent                |    BBox        |    Extent of the dataset. Must be WSG84.                                                                                                 |
|    source                |    string      |    Contract partner for original data e.g. swisstopo, Canton xy...                                                                       |
|    metadata              |    string      |    URI to pdf or fileshare with several pdfs containing aditional   Metadata                                                             |
|    access                |    string      |    URI to the Detailed view of the record in GeoVITe or HSR Portal                                                                       |
|    collection            |    string      |    Group name or feature dataset                                                                                                         |
|    dataset               |    string      |    Service, dataset or file name                                                                                                         |
|    service               |    string      |    Service type e.g. ETH Geovite, WMS HSR-Geoportal...                                                                                   |
|    crs                   |    string      |    CRS of original data (EPSG)                                                                                                           |
|    terms                 |    string      |    URI to PDF with information about the terms of use                                                                                    |
|    proved                |    date        |    Most recent proving date                                                                                                              |
|    modified              |    dateTime    |    Most recent modification time                                                                                                         |
|    login_name            |    string      |    Metadata Author name                                                                                                                  |
|    visibility            |    string      |    Metadata visibility in front end                                                                                                      |
|    geodata_type          |    string      |    e.g. point, raster, vector...      