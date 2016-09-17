from django.contrib import admin

# Register your models here.
from django.contrib.admin.utils import flatten_fieldsets

from api.models import RecordTag, CombinedRecord, Record


class ReadOnlyAdmin(admin.ModelAdmin):
    change_form_template = 'api/admin/change_form.html'
    actions = None

    def get_readonly_fields(self, request, obj=None):

        if hasattr(self, 'declared_fieldsets') and self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class RecordAdminMixin(object):
    readonly_fields = ['api_id', 'tag_list']
    list_display = ['api_id', 'language', 'content', 'publication_year', 'abstract', 'tag_list']
    exclude = ['search_vector_de', 'search_vector_fr', 'search_vector_en']
    search_fields = ['search_vector_de', 'search_vector_fr', 'search_vector_en']


class RecordTagAdmin(admin.ModelAdmin):
    exclude = ['tag_de_search_vector', 'tag_en_search_vector', 'tag_fr_search_vector']
    list_display = ['tag_de', 'tag_en', 'tag_fr', ]
    search_fields = ['tag_de_search_vector', 'tag_en_search_vector', 'tag_fr_search_vector']
admin.site.register(RecordTag, RecordTagAdmin)


class RecordAdmin(RecordAdminMixin, admin.ModelAdmin):
    pass
admin.site.register(Record, RecordAdmin)


class CombinedRecordAdmin(RecordAdminMixin, ReadOnlyAdmin):
    pass
admin.site.register(CombinedRecord, CombinedRecordAdmin)
