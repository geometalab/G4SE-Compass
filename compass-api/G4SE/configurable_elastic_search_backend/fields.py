from haystack.fields import CharField as BaseCharField


class ConfigurableFieldMixin(object):
    def __init__(self, **kwargs):
        self.analyzer = kwargs.pop('analyzer', None)
        super(ConfigurableFieldMixin, self).__init__(**kwargs)


class CharField(ConfigurableFieldMixin, BaseCharField):
    pass
