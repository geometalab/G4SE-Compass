import pytest
import requests

from expectation_tests.helpers import ordered

result_expectations = [
    'equal',
    'gt',
    'gte',
    'lt',
    'lte',
]

search_params_expectation = [
    dict(search_request='', expected_count=137, comparison='gte'),
    dict(search_request='?language=en&search=swixerland~', expected_count=30, comparison='gt'),

    # equal 2, 3
    dict(search_request='?language=en&search=digital%20AND%20orthophoto', expected_count=4, comparison='gte'),
    dict(search_request='?language=en&search=digital%20orthophoto', expected_count=4, comparison='gte'),

    dict(search_request='?language=en&search=digital%20OR%20orthophoto', expected_count=21, comparison='gte'),

    # equal 5, 6
    dict(search_request='?language=en&search=digital%20NOT%20orthophoto', expected_count=16, comparison='gte'),
    dict(search_request='?language=en&search=digital%20AND%20NOT%20orthophoto', expected_count=16, comparison='gte'),

    dict(search_request='?language=en&search=tr*', expected_count=22, comparison='gte'),
    dict(search_request='?language=en&search="Pfäffikon%20ZH"', expected_count=0, comparison='equal'),

    # equal, but different ordering: 9, 10
    dict(search_request='?language=en&page_size=100&search=digital&ordering=-modified', expected_count=30,
         comparison='gte'),
    dict(search_request='?language=en&page_size=100&search=digital&ordering=title', expected_count=30,
         comparison='gte'),

    # another filtering and sorting example: 11, 12
    dict(search_request='?language=en&search=Switzerland&service_type=MapService', expected_count=30, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&service_type=MapService&ordering=-title', expected_count=30,
         comparison='gte'),

    # "drilldown" example, 13, 14, 15
    dict(search_request='?language=en&search=Switzerland', expected_count=100, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&service_type=MapService', expected_count=30, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&service_type=MapService&dataset=TLM_SCHUTZGEBIET',
         expected_count=1, comparison='gte'),

    # years example, all equal: 16, 17, 18
    dict(search_request='?language=en&search=Switzerland&publication_year=2015', expected_count=8, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&to_year=2015&from_year=2015', expected_count=8,
         comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&to_year=2015&from_year=2015&publication_year=2015',
         expected_count=8, comparison='gte'),

    # years example, "drilldown": 19, 20, 21
    dict(search_request='?language=en&search=Switzerland&publication_year=2016', expected_count=50, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&publication_year=2016&service_type=MapService',
         expected_count=30, comparison='gte'),
    dict(search_request='?language=en&search=Switzerland&publication_year=2016&service_type=MapService&dataset=TLM_SCHUTZGEBIET',
         expected_count=1, comparison='gte'),

    # equal, but different ordering: 22, 23
    dict(search_request='?language=en&page_size=100&search=digital&ordering=-title', expected_count=30,
         comparison='gte'),
    dict(search_request='?language=en&page_size=100&search=digital&ordering=title', expected_count=30,
         comparison='gte'),
]

API_SEARCH_ENDPOINT = '/api/search/'


@pytest.fixture(params=search_params_expectation)
def search_request(request):
    param = request.param
    return param['search_request'], param['expected_count'], param['comparison']


@pytest.fixture()
def api_call(search_request, host):
    search_param, expected_count, comparison = search_request
    request = host + API_SEARCH_ENDPOINT + search_param
    response = requests.get(request)
    resulting_json = response.json()
    return search_param, expected_count, comparison, resulting_json['count'], resulting_json['results']


def test_searches(api_call):
    search_param, expected_count, comparison, count, _ = api_call
    assert comparison in result_expectations

    if comparison == 'equal':
        assert count == expected_count
    elif comparison == 'gt':
        assert count > expected_count
    elif comparison == 'gte':
        assert count >= expected_count
    elif comparison == 'lt':
        assert count < expected_count
    elif comparison == 'lte':
        assert count <= expected_count
    elif comparison == 'is':
        assert count is expected_count


def test_search_variants(host):
    search_params1 = search_params_expectation[2]
    search_params2 = search_params_expectation[3]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    assert count1 == count2
    assert result1 == result2

    search_params1 = search_params_expectation[5]
    search_params2 = search_params_expectation[6]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    assert count1 == count2
    assert result1 == result2

    search_params1 = search_params_expectation[9]
    search_params2 = search_params_expectation[10]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    assert count1 == count2
    assert result1 != result2  # result should be differently ordered

    search_params1 = search_params_expectation[11]
    search_params2 = search_params_expectation[12]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    assert count1 == count2
    assert result1 != result2

    search_params1 = search_params_expectation[13]
    search_params2 = search_params_expectation[14]
    search_params3 = search_params_expectation[15]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    search_params3 = search_params3['search_request'], search_params3['expected_count'], search_params3['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    _, _, _, count3, result3 = api_call(search_params3, host)
    assert count1 > count2 > count3

    search_params1 = search_params_expectation[16]
    search_params2 = search_params_expectation[17]
    search_params3 = search_params_expectation[18]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    search_params3 = search_params3['search_request'], search_params3['expected_count'], search_params3['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    _, _, _, count3, result3 = api_call(search_params3, host)
    assert count1 == count2 == count3
    assert ordered(result1) == ordered(result2) == ordered(result3)

    search_params1 = search_params_expectation[19]
    search_params2 = search_params_expectation[20]
    search_params3 = search_params_expectation[21]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    search_params3 = search_params3['search_request'], search_params3['expected_count'], search_params3['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    _, _, _, count3, result3 = api_call(search_params3, host)
    assert count1 > count2 > count3

    search_params1 = search_params_expectation[22]
    search_params2 = search_params_expectation[23]
    search_params1 = search_params1['search_request'], search_params1['expected_count'], search_params1['comparison']
    search_params2 = search_params2['search_request'], search_params2['expected_count'], search_params2['comparison']
    _, _, _, count1, result1 = api_call(search_params1, host)
    _, _, _, count2, result2 = api_call(search_params2, host)
    assert count1 == count2
    assert result1 != result2
