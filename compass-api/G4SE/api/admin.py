from django.contrib import admin

# Register your models here.
from api.models import RecordTag


class RecordTagAdmin(admin.ModelAdmin):
    exclude = ['tag_de_search_vector', 'tag_en_search_vector', 'tag_fr_search_vector']
    list_display = ['tag_de', 'tag_en', 'tag_fr', ]
    search_fields = ['tag_de_search_vector', 'tag_en_search_vector', 'tag_fr_search_vector']

admin.site.register(RecordTag, RecordTagAdmin)
