# API

Base URL: XXX
## record
| Get a specific record by id |                                      |
|-----------------------------|--------------------------------------|
| Path                        | /api/record/:id                      |
| Parameters                  | Required: id                         |
| Result                      | Record                               |
| Example                     | /api/record/1234151                  |

## search
| Fulltext search records |                                     |
|-------------------------|-------------------------------------|
| Path                    | /api/search/                        |
| Parameters              | Required: query, optional: language |
| Result                  | Record list                         |
| Example                 | /api/search?query=wald;language=en  |

* The language parameter indicates the language of the search query, not the result. Only keywords are stored multilingual.

## recent
| Get most rectly inserted records |                        |
|----------------------------------|------------------------|
| Path                             | /api/recent/           |
| Parameters                       | Optional: amount       |
| Result                           | Record list            |
| Example                          | /api/search?amount=10  |