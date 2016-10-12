from django import forms
from django.contrib import admin

from api.models import TranslationTag, GeoServiceMetadata, GEO_SERVICE_METADATA_AGREED_FIELDS


class EditableGeoServiceMetadataForm(forms.ModelForm):
    def clean(self):
        cleaned_values = super().clean()
        for key, value in cleaned_values.items():
            if value == '':
                cleaned_values[key] = None
        return cleaned_values

    class Meta:
        model = GeoServiceMetadata
        fields = GEO_SERVICE_METADATA_AGREED_FIELDS[1:-1]


class RecordTagAdmin(admin.ModelAdmin):
    list_display = ['tag_de', 'tag_en', 'tag_fr', 'tag_alternatives_de', 'tag_alternatives_en', 'tag_alternatives_fr', ]
    search_fields = ['tag_de', 'tag_en', 'tag_fr', 'tag_alternatives_de', 'tag_alternatives_en', 'tag_alternatives_fr', ]
admin.site.register(TranslationTag, RecordTagAdmin)


class GeoServiceMetadataAdmin(admin.ModelAdmin):
    readonly_fields = ['api_id', 'tag_list_display']
    list_display = ['api_id', 'language', 'title', 'publication_year', 'abstract', 'tag_list_display', 'modified']
    form = EditableGeoServiceMetadataForm
    list_per_page = 10
    list_filter = ['language', 'publication_year']
    search_fields = GEO_SERVICE_METADATA_AGREED_FIELDS
    ordering = ['-modified', ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(imported=False)
admin.site.register(GeoServiceMetadata, GeoServiceMetadataAdmin)


class ReadOnlyGeoServiceMetadata(GeoServiceMetadata):
    """
    This has no restrictions when viewed through the admin, but shouldn't be edited.
    """
    class Meta:
        proxy = True


class ReadOnlyGeoServiceMetadataAdmin(admin.ModelAdmin):
    actions = None
    change_form_template = 'api/admin/change_form.html'

    list_display = ['api_id', 'language', 'title', 'publication_year', 'abstract', 'tag_list_display', 'modified']
    list_per_page = 10
    list_filter = ['language', 'publication_year']
    ordering = ['-modified', ]
    search_fields = GEO_SERVICE_METADATA_AGREED_FIELDS
    readonly_fields = GEO_SERVICE_METADATA_AGREED_FIELDS
    fields = GEO_SERVICE_METADATA_AGREED_FIELDS
admin.site.register(ReadOnlyGeoServiceMetadata, ReadOnlyGeoServiceMetadataAdmin)
