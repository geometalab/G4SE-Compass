from haystack.exceptions import NotHandled
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
from haystack.signals import RealtimeSignalProcessor

from api.models import GeoServiceMetadataTagItem, TranslationTag, GeoServiceMetadata


def retag_all():
    GeoServiceMetadataTagItem.objects.all().delete()
    for tag in TranslationTag.objects.all():
        add_tag_to_records(tag)


def add_tag_to_records(tag_instance):
    # a new tag, find in all records and tag them accordingly
    for metadata_entry in _taggable_geo_metadata(tag_instance):
        GeoServiceMetadataTagItem.objects.create(
            tag=tag_instance,
            geo_service_metadata=metadata_entry,
        )


def changed_or_added_tag_update_records_signal(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    if not created:
        # updated tag
        # remove old tags and do the same as if it were a new tag
        GeoServiceMetadataTagItem.objects.filter(tag=instance).delete()
    # a new tag, find in all records and tag them accordingly
    add_tag_to_records(instance)


def _search_query_string(tag):
    de_tags = tag.tag_alternatives_de
    de_tags.append(tag.tag_de)
    en_tags = tag.tag_alternatives_en
    en_tags.append(tag.tag_en)
    fr_tags = tag.tag_alternatives_fr
    fr_tags.append(tag.tag_fr)
    return {
        GeoServiceMetadata.GERMAN: ' OR '.join(de_tags),
        GeoServiceMetadata.ENGLISH: ' OR '.join(en_tags),
        GeoServiceMetadata.FRENCH: ' OR '.join(fr_tags),
    }


def _search_query(language, search_query):
    result_queryset = SearchQuerySet().using(language).filter(text=Raw(search_query[language])).models(GeoServiceMetadata)
    return result_queryset


def _taggable_geo_metadata(tag):
    search_texts = _search_query_string(tag)
    result_de = list(_search_query(GeoServiceMetadata.GERMAN, search_texts).values_list('api_id', flat=True))
    result_en = list(_search_query(GeoServiceMetadata.ENGLISH, search_texts).values_list('api_id', flat=True))
    result_fr = list(_search_query(GeoServiceMetadata.FRENCH, search_texts).values_list('api_id', flat=True))
    results = list(set(result_de + result_en + result_fr))
    return GeoServiceMetadata.objects.filter(api_id__in=results)


def _is_tag_in_geoservice_metadata(tag, metadata):
    search_texts = _search_query_string(tag)
    query_result = list(_search_query(metadata.language, search_texts).values_list('api_id', flat=True))

    # UUID class, but in index is a CharField ~> can only be compared as string
    comparable_api_id = str(metadata.api_id)
    return comparable_api_id in query_result


def _tags_for_geoservice_metadata(metadata):
    tags = []
    for tag in TranslationTag.objects.all():
        if _is_tag_in_geoservice_metadata(tag, metadata):
            tags.append(tag)
    return list(set(tags))


def changed_or_added_geo_service_metadata_update_tag(sender, instance):
    # remove existing tags
    GeoServiceMetadataTagItem.objects.filter(geo_service_metadata=instance).delete()

    # a new tag, find in all records and tag them accordingly
    for tag in _tags_for_geoservice_metadata(instance):
        GeoServiceMetadataTagItem.objects.create(
            tag=tag,
            geo_service_metadata=instance,
        )


class GeoServiceMetadataRealtimeSignalProcessor(RealtimeSignalProcessor):
    def _using_backend(self, instance):
        if isinstance(instance, GeoServiceMetadata):
            using_backends = [GeoServiceMetadata.GERMAN, GeoServiceMetadata.ENGLISH, GeoServiceMetadata.FRENCH]
        else:
            using_backends = self.connection_router.for_write(instance=instance)
        return using_backends

    def _update_index(self, sender, instance):
        using_backends = self._using_backend(instance)
        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.update_object(instance, using=using)
            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def handle_save(self, sender, instance, **kwargs):
        if isinstance(instance, GeoServiceMetadata):
            self._update_index(sender, instance)
            changed_or_added_geo_service_metadata_update_tag(sender, instance)
            self._update_index(sender, instance)

    def handle_delete(self, sender, instance, **kwargs):
        using_backends = self._using_backend(instance)

        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.remove_object(instance, using=using)
            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass
