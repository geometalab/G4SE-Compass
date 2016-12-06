import pytest

from api.models import GeoServiceMetadata, TranslationTag


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
        title=placeholder_string,
        abstract=placeholder_string,
        publication_year=2014,
        geography=placeholder_string,
        geodata_type=placeholder_string,
        source=placeholder_string,
        metadata_link=placeholder_url,
        access_link=placeholder_url,
        crs=crs,
        term_link=placeholder_url,
        visibility=GeoServiceMetadata.VISIBILITY_PUBLIC,
    )


@pytest.fixture
def record_en(db, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['title'] = 'Some generalized content'
    kwargs['abstract'] = 'Some english abstract, about digital a house.'
    kwargs['language'] = GeoServiceMetadata.ENGLISH
    record, _ = GeoServiceMetadata.objects.get_or_create(**kwargs)
    yield record
    record.delete()


@pytest.fixture
def record_de(db, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['title'] = 'Inhaltsbeschreibung'
    kwargs['abstract'] = 'Ein währschafter Inhalt, so richtig digital deftig.'
    kwargs['language'] = GeoServiceMetadata.GERMAN
    record, _ = GeoServiceMetadata.objects.get_or_create(**kwargs)
    yield record
    record.delete()


@pytest.fixture
def record_fr(db, record_default_kwargs):
    kwargs = record_default_kwargs.copy()
    kwargs['title'] = 'Un example du contenue'
    kwargs['abstract'] = 'Ce abstract digital example maisons.'
    kwargs['language'] = GeoServiceMetadata.FRENCH
    record, _ = GeoServiceMetadata.objects.get_or_create(**kwargs)
    yield record
    record.delete()


@pytest.fixture
def one_tag_for_them_all(db):
    tag = TranslationTag.objects.create(
        tag_de='inhalt', tag_en='house', tag_fr='maison'
    )
    yield tag
    tag.delete()


@pytest.fixture
def tag_that_only_tags_german(db):
    tag = TranslationTag.objects.create(
        tag_de='inhalt', tag_en='other', tag_fr='autre'
    )
    yield tag
    tag.delete()


@pytest.fixture
def tag_that_only_tags_french(db):
    tag = TranslationTag.objects.create(
            tag_de='achtung', tag_en='another', tag_fr='example'
        )
    yield tag
    tag.delete()


@pytest.fixture
def tag_that_matches_all_languages(db):
    tag = TranslationTag.objects.create(
            tag_de='digital', tag_en='some', tag_fr='differente'
        )
    yield tag
    tag.delete()


def test_tagging_all(record_de, record_en, record_fr, one_tag_for_them_all):
    """
    A bit a long test, since it tests various interactions.
    """
    assert record_de.tag_list_display() == record_en.tag_list_display()
    assert record_de.tag_list_display() == record_fr.tag_list_display()
    assert one_tag_for_them_all.id == record_de.tags.all()[0].id


def test_tagging_german_language_only(record_de, record_en, record_fr, tag_that_only_tags_german):
    assert record_de.tags.all()[0].id == tag_that_only_tags_german.id
    assert list(record_fr.tags.all()) == []
    assert list(record_en.tags.all()) == []


def test_tagging_french_language_only(record_de, record_en, record_fr, tag_that_only_tags_french):
    assert record_fr.tags.all()[0].id == tag_that_only_tags_french.id
    assert list(record_de.tags.all()) == []
    assert list(record_en.tags.all()) == []


def test_tagging_identical_key(record_de, record_en, record_fr, tag_that_matches_all_languages):
    """
    since "digital" is in every language, this will tag every
    language.
    """
    assert record_en.tags.all()[0].id == record_fr.tags.all()[0].id == record_de.tags.all()[0].id == \
        tag_that_matches_all_languages.id
