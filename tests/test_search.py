import pytest
from search import search
from db import connect_db

def test_search_rooms():
    test_res = search(rooms=2)
    if not test_res:
        pytest.fail("Список пуст")
    for apartment in test_res:
        assert apartment[3] == 2

def test_search_pets_allowed_0():
    test_res = search(pets_allowed=0)
    assert len(test_res) == len(search())

def test_search_pets_allowed_1():
    test_res = search(pets_allowed=1)
    if not test_res:
        pytest.fail("Список пуст")
    for apartment in test_res:
        assert apartment[5] == 1

def test_price():
    test_res = search(price=40000)
    if not test_res:
        pytest.fail("Список пуст")
    for apartment in test_res:
        assert apartment[0] <= 40000

def test_search_district():
    district = ["Басманный", "Отрадное"]
    test_res = search(district=district)
    if not test_res:
        pytest.fail("Список пуст")
    for apartment in test_res:
        assert apartment[1] in district

def test_search_metro():
    metro = ["Отрадное", "Курская"]
    test_res = search(metro=metro)
    if not test_res:
        pytest.fail("Список пуст")
    for apartment in test_res:
        assert apartment[2] in metro

def test_search():
    with connect_db() as conn:
        sql_list = conn.execute("SELECT * FROM appart").fetchall()
    test_res = search()
    assert len(test_res) == len(sql_list)


def test_search_district_not_found():
    district = ["abc"]
    test_res = search(district=district)
    if not test_res:
        assert len(test_res) == 0