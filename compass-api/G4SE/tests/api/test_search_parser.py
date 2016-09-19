import pytest
from django.db.models.expressions import CombinedExpression

from api.search_parser import search_query_parser
from api.search_parser.patched_search_query import SearchQuery
from api.search_parser.query_parser import SearchSemantics


def _parenthesized_str(self):
    return "({} {} {})".format(self.lhs, self.connector, self.rhs)
CombinedExpression.__str__ = _parenthesized_str


def assert_search_query(input_string, expected_tokens, expected_value=None):
    val = search_query_parser.UnknownParser().parse(input_string)
    assert val == expected_tokens
    if expected_value is not None:
        val = search_query_parser.UnknownParser().parse(input_string, semantics=SearchSemantics())
        assert str(val) == str(expected_value)


@pytest.fixture(params=[
    ['a', 'a', SearchQuery('a')],
    ['foo', 'foo', SearchQuery('foo')],
    ['a&b', ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b')],
    ['!a', ['!', 'a'], ~SearchQuery('a')],
    ['!a&b', ['!', 'a', '&', 'b'], (~SearchQuery('a')) & SearchQuery('b')],
    ['a & b', ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b')],
    ['! a', ['!', 'a'], ~SearchQuery('a')],
    ['! a & b', ['!', 'a', '&', 'b'], (~SearchQuery('a')) & SearchQuery('b')],
    ["'a & (!b | !c) & d | e'", "'a & (!b | !c) & d | e'", SearchQuery("a & (!b | !c) & d | e")],
    ['"a & (!b | !c) & d | e"', '"a & (!b | !c) & d | e"', SearchQuery("a & (!b | !c) & d | e")],
    ['""', '""', SearchQuery("")],
    ["''", "''", SearchQuery("")],
    ["'\"'", "'\"'", SearchQuery('"')],
    ['"\'"', '"\'"', SearchQuery("'")],
    [r"'\''", r"'\''", SearchQuery("'")],
    ['a b', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b')],
    ['a  b', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b')],
    ['a\t b', ['a', '\t', 'b'], SearchQuery('a') | SearchQuery('b')],
    ['a \tb', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b')],
    ['foo  bar', ['foo', ' ', 'bar'], SearchQuery('foo') | SearchQuery('bar')],
    ["(a)", 'a', SearchQuery('a')],
    ["((a))", 'a', SearchQuery('a')],
    ["(a & b)", ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b')],
    [
        "a & (b & c)", ['a', '&', ['b', '&', 'c']],
        SearchQuery('a') & (SearchQuery('b') & SearchQuery('c'))
    ],
    [
        "(a | b) & (c | d)", ['a', '|', 'b', '&', ['c', '|', 'd']],
        (SearchQuery('a') | SearchQuery('b')) & (SearchQuery('c') | SearchQuery('d'))
    ],
    [
        "(a | b) & (c | d) & (f | g)", ['a', '|', 'b', '&', ['c', '|', 'd'], '&', ['f', '|', 'g']],
        (SearchQuery('a') | SearchQuery('b')) & (SearchQuery('c') | SearchQuery('d')) & (SearchQuery('f') | SearchQuery('g'))
    ],
    [
        "((a | b) & (c | d)) & (f | g)", ['a', '|', 'b', '&', ['c', '|', 'd'], '&', ['f', '|', 'g']],
        ((SearchQuery('a') | SearchQuery('b')) & (SearchQuery('c') | SearchQuery('d'))) & (SearchQuery('f') | SearchQuery('g'))
    ],
    [
        "((a | b) & (c | d)) | (f | g)", ['a', '|', 'b', '&', ['c', '|', 'd'], '|', ['f', '|', 'g']],
        ((SearchQuery('a') | SearchQuery('b')) & (SearchQuery('c') | SearchQuery('d')) | (SearchQuery('f') | SearchQuery('g')))
    ],
    [
        "a & (!b | !c) & d | e", ['a', '&', ['!', 'b', '|', ['!', 'c']], '&', 'd', '|', 'e'],
        SearchQuery('a') & (~SearchQuery('b') | ~SearchQuery('c')) & SearchQuery('d') | SearchQuery('e')
    ],
    [
        "!'a & (!b | !c) & d | e' & f | k", ['!', "'a & (!b | !c) & d | e'", '&', 'f', '|', 'k'],
        ~SearchQuery('a & (!b | !c) & d | e') & SearchQuery('f') | SearchQuery('k')
    ]

])
def search_query(request):
    return request.param


def test_search_queries(search_query):
    assert_search_query(*search_query)
