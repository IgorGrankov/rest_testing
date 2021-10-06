import pytest
from requests import HTTPError

from tests.api_client import ApiClient

api = ApiClient()


def test_planets_default():
    default_next_pagination_value = "page=2"
    default_planets_count = 60
    default_results_len = 10
    resp = api.get_planets()

    assert resp.results, "Results are empty"
    assert resp.count == default_planets_count, "Count is wrong"
    assert len(resp.results) == default_results_len, "Results len is wrong"
    assert default_next_pagination_value in resp.next, "Pagination 'next' value is wrong"
    assert not resp.previous, "Pagination 'previous' value is wrong"


def test_planets_search():
    expected_results_len = 1
    expected_count = 1
    planet_name = "Naboo"

    resp = api.get_planets(planet_name)
    results = resp.results[0]

    assert len(resp.results) == expected_results_len, "Results list len is wrong"
    assert planet_name in results.name, "Search results are wrong"
    assert resp.count == expected_count, "Count is wrong"
    assert not resp.next, "Pagination 'next' value is wrong"
    assert not resp.previous, "Pagination 'previous' value is wrong"


def test_planets_pagination():
    page = "page=2"
    default_next_pagination_value = "page=3"
    default_previous_pagination_value = "page=1"

    resp = api.get_planets(None, page)

    assert resp.results, "Results are empty"
    assert default_next_pagination_value in resp.next, "Pagination 'next' value is wrong"
    assert default_previous_pagination_value in resp.previous, "Pagination 'previous' value is wrong"


def test_planets_search_no_data():
    planet_name = "Syktivkar"

    resp = api.get_planets(planet_name)

    assert len(resp.results) == 0, "Results list len is wrong"
    assert not resp.count, "Count is wrong"
    assert not resp.next, "Pagination 'next' value is wrong"
    assert not resp.previous, "Pagination 'previous' value is wrong"


def test_planets_id():
    planet_id = 1
    expected_name = "Tatooine"

    resp = api.get_planets_id(planet_id)

    assert str(planet_id) in resp.url, "Url is wrong for planet id"
    assert resp.name == expected_name, "Name is wrong for planet id"


def test_planets_wrong_id():
    planet_id = "test string"

    with pytest.raises(HTTPError):
        api.get_planets_id(planet_id)


