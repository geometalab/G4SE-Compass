from django.apps import AppConfig
from django.db.models.signals import post_save


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from api.signals import auto_tag_tags_signal
        # registering signals with the model's string label
        post_save.connect(auto_tag_tags_signal, sender='api.RecordTag')
