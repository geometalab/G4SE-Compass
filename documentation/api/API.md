# API

Base URL: http://86.119.37.75/
## metadata record
| Get a specific metadata record by id |                             |
|-----------------------------|--------------------------------------|
| Path                        | /api/metadata/:id                    |
| Parameters                  | Required: id                         |
| Result                      | Record                               |
| Example                     | /api/metadata/1234151                |

## all metadata records
| Get all metadata records   |                                       |
|-----------------------------|--------------------------------------|
| Path                        | /api/metadata/                       |
| Parameters                  | None                                 |
| Result                      | Record list                          |
| Example                     | /api/metadata/                       |

## search
| Fulltext search records |                                         |
|-------------------------|-----------------------------------------|
| Path                    | /api/search/                            |
| Parameters              | Required: query, optional: language     |
| Result                  | Record list                             |
| Example                 | /api/search?query=wildlife&language=en  |

## recent
| Get most rectly inserted records |                        |
|----------------------------------|------------------------|
| Path                             | /api/recent/           |
| Parameters                       | Optional: count        |
| Result                           | Record list            |
| Example                          | /api/search?count=10   |
