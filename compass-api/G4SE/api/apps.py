from django.apps import AppConfig
from django.db.models.signals import post_save


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from api.signals import changed_or_added_tag_update_records_signal
        # registering signals with the model's string label
        post_save.connect(changed_or_added_tag_update_records_signal, sender='api.TranslationTag')
