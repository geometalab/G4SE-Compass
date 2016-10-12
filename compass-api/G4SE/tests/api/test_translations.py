import pytest

from api.models import Record, TranslationTag


@pytest.fixture
def placeholder_string():
    return 'PLACEHOLDER'


@pytest.fixture
def placeholder_url():
    return 'http://example.com'


@pytest.fixture
def crs():
    return 'EPSG:4326'  # WGS84


@pytest.fixture
def record_default_kwargs(placeholder_string, placeholder_url, crs):
    return dict(
        identifier=placeholder_string,
        content=placeholder_string,
        abstract=placeholder_string,
        publication_year=placeholder_string,
        geography=placeholder_string,
        geodata_type=placeholder_string,
        source=placeholder_string,
        metadata_link=placeholder_url,
        access_link=placeholder_url,
        crs=crs,
        term_link=placeholder_url,
        visibility=Record.PUBLIC,
    )


@pytest.fixture
def record_en(setup_database, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['content'] = 'Some generalized content'
    kwargs['abstract'] = 'Some english abstract, about digital housing'
    kwargs['language'] = Record.ENGLISH
    record, _ = Record.objects.get_or_create(**kwargs)
    return record


@pytest.fixture
def record_de(setup_database, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['content'] = 'Inhaltsbeschreibung'
    kwargs['abstract'] = 'Ein währschafter Inhalt, so richtig digital deftig.'
    kwargs['language'] = Record.GERMAN
    record, _ = Record.objects.get_or_create(**kwargs)
    return record


@pytest.fixture
def record_fr(setup_database, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['content'] = 'Un example du contenue'
    kwargs['abstract'] = 'Ce abstract digital example maisons.'
    kwargs['language'] = Record.FRENCH
    record, _ = Record.objects.get_or_create(**kwargs)
    return record


def test_tagging_all(record_de, record_en, record_fr):
    """
    A bit a long test, since it tests various interactions.
    """
    assert list(record_de.tags) == list(record_en.tags) == list(record_fr.tags) == []
    one_tag_for_them_all = TranslationTag.objects.create(
        tag_de='inhalt', tag_en='house', tag_fr='maison'
    )
    assert record_de.tag_list_display() == record_en.tag_list_display()
    assert record_de.tag_list_display() == record_fr.tag_list_display()
    assert one_tag_for_them_all.id == record_de.tags[0].record_tag.id

    one_tag_for_them_all.delete()
    assert list(record_de.tags) == list(record_en.tags) == list(record_fr.tags) == []


def test_tagging_one_language_only(record_de, record_en, record_fr):
    tag_that_only_tags_german = TranslationTag.objects.create(
        tag_de='inhalt', tag_en='other', tag_fr='autre'
    )
    assert record_de.tags[0].record_tag.id == tag_that_only_tags_german.id
    assert list(record_fr.tags) == []
    assert list(record_en.tags) == []
    tag_that_only_tags_german.delete()

    tag_that_only_tags_french = TranslationTag.objects.create(
        tag_de='achtung', tag_en='other', tag_fr='example'
    )
    assert record_fr.tags[0].record_tag.id == tag_that_only_tags_french.id
    assert list(record_de.tags) == []
    assert list(record_en.tags) == []
    tag_that_only_tags_french.delete()


def test_tagging_identical_key(record_de, record_en, record_fr):
    """
    since "digital" is in every language, this will tag every
    language.
    """
    tag_that_only_tags_french = TranslationTag.objects.create(
        tag_de='digital', tag_en='other', tag_fr='autre'
    )
    assert record_en.tags[0].record_tag.id == \
           record_fr.tags[0].record_tag.id == \
           record_de.tags[0].record_tag.id == \
           tag_that_only_tags_french.id
    tag_that_only_tags_french.delete()
