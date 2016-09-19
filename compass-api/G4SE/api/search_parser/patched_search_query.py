from django.contrib.postgres.search import SearchQuery


class MySearchQuery(SearchQuery):
    def __repr__(self):
        s = super().__repr__()
        if self.invert:
            s = "!{}".format(s)
        return s
SearchQuery = MySearchQuery
