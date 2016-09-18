from django.contrib.postgres.search import SearchQuery
from django.db.models import Q

from api.models import Record, RecordTaggedItem, RecordTag


def changed_or_added_tag_update_records_signal(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    if not created:
        # updated tag
        # remove old tags and do the same as if it were a new tag
        RecordTaggedItem.objects.filter(record_tag=instance).delete()

    # a new tag, find in all records and tag them accordingly
    for record in _taggable_records(instance):
        RecordTaggedItem.objects.create(
            record_tag=instance,
            content_object=record,
        )


def _combined_query(main_tag, tags, language):
    q = SearchQuery(main_tag, config=language)
    for tag in tags:
        q = q | SearchQuery(tag, config=language)
    return q


def _search_vector(tag):
    return {
        Record.GERMAN: Q(search_vector_de=_combined_query(tag.tag_de, tag.tag_alternatives_de, 'german')),
        Record.ENGLISH: Q(search_vector_en=_combined_query(tag.tag_en, tag.tag_alternatives_en, 'english')),
        Record.FRENCH: Q(search_vector_fr=_combined_query(tag.tag_fr, tag.tag_alternatives_fr, 'french')),
    }


def _taggable_records(tag):
    search_vector = _search_vector(tag)
    search_de, search_en, search_fr = search_vector[Record.GERMAN], search_vector[Record.ENGLISH], search_vector[Record.FRENCH]
    return Record.objects.filter(search_de | search_en | search_fr)


def _is_tag_in_record(tag, record):
    search_vector = _search_vector(tag)[record.language]
    return Record.objects.filter(api_id=record.api_id).filter(search_vector).count() > 0


def _tags_for_record(record):
    tags = []
    for tag in RecordTag.objects.all():
        if _is_tag_in_record(tag, record):
            tags.append(tag)
    return list(set(tags))


def changed_or_added_record_update_tag_signal(sender, instance, created, *args, **kwargs):
    if not created:
        # updated tag
        # remove old tags and do the same as if it were a new tag
        RecordTaggedItem.objects.filter(object_id=instance.api_id).delete()

    # a new tag, find in all records and tag them accordingly
    for tag in _tags_for_record(instance):
        RecordTaggedItem.objects.create(
            record_tag=tag,
            content_object=instance,
        )
