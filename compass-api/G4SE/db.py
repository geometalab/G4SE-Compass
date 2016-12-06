from django.db.models import Func, FloatField


class VectorFieldSearchRank(Func):
    function = 'ts_rank_cd'
    _output_field = FloatField()

    def __init__(self, vector_field_name, query, **extra):
        super(VectorFieldSearchRank, self).__init__(vector_field_name, query, **extra)

    def as_sql(self, compiler, connection, function=None, template=None):
        extra_params = []
        extra_context = {}
        sql, params = super(VectorFieldSearchRank, self).as_sql(
            compiler, connection,
            function=function, template=template, **extra_context
        )
        return sql, extra_params + params
