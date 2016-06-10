# API

Base URL: XXX
## record
| Get a specific record by id |                                      |
|-----------------------------|--------------------------------------|
| Path                        | /api/record/:id                      |
| Parameters                  | Required: id                         |
| Notes                       |                                      |
| Result                      | Record                               |
| Example                     | /api/record/1234151                  |

## search
| Fulltext search records |                          |
|-------------------------|--------------------------|
| Path                    | /api/search/             |
| Parameters              | Required: query          |
| Result                  | Record list              |
| Example                 | /api/search/?query=wald  |

## recent
| Get most rectly inserted records |                        |
|----------------------------------|------------------------|
| Path                             | /api/recent/           |
| Parameters                       | Optional: amount       |
| Result                           | Record list            |
| Example                          | /api/search/?amound=10 |
