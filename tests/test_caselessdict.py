import os
import pickle

from collections.abc import Mapping
from copy import copy
from pytest import raises
from sys import getsizeof
from tempfile import NamedTemporaryFile
from typing import TypeVar

from caseless import CaselessDict

T = TypeVar("T")

def round_trip_pickle(obj: T) -> T:
    temp = NamedTemporaryFile("w", delete=False)
    with open(temp.name, "wb") as handle:
        pickle.dump(obj, handle)
    with open(temp.name, "rb") as handle:
        rehydrated = pickle.load(handle)
    os.remove(temp.name)
    return rehydrated

class TestCaselessDict(object):
    def test_isinstance(self):
        assert isinstance(CaselessDict(), Mapping)

    def test_accepts_type_params(self):
        CaselessDict[int, int]({1: 1})

    def test__setitem__(self):
        with raises(TypeError):
            exec("CaselessDict()[1] = 2")

    def test__delitem__(self):
        with raises(TypeError):
            exec("del CaselessDict({1: 2})[1]")

    def test_pop(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).pop(1)")

    def test_popitem(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).popitem()")

    def test_clear(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).clear()")

    def test_update(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).update(1, 3)")

    def test_setdefault(self):
        with raises(AttributeError):
            exec("CaselessDict({1: 2}).setdefault(1)")

    def test__contains__(self):
        assert "key" in CaselessDict({"key": "value"})
        assert "key" in CaselessDict(key="value")
        assert "key" in CaselessDict(KEY="value")  # Case invariant
        assert "keY" in CaselessDict(KEY="value")  # Case invariant
        assert "KeY" in CaselessDict(KEY="value")  # Case invariant
        assert "key" in CaselessDict({"KEY": "value"})
        assert "key" not in CaselessDict()

        assert 2 in CaselessDict({2: "value"})
        assert 2 not in CaselessDict()

    def test__copy__(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping == copy(mapping)
        assert mapping.get(2) == copy(mapping).get(2)
        assert mapping.get(4) == copy(mapping).get(4)
        assert mapping.get(5) == copy(mapping).get(5)
        assert mapping.get("LOWER") == copy(mapping).get("lower")

    def test__eq__(self):
        CaselessDict({1: 2}) == CaselessDict({1: 2})
        CaselessDict({1: 2}) != CaselessDict({3: 4})
        CaselessDict({"lower": "UPPER"}) == CaselessDict({"LOWER": "UPPER"})
        CaselessDict({1: 2, "lower": "UPPER"}) != CaselessDict({3: 4, "LOWER": "UPPER"})

    def test__getitem__(self):
        assert CaselessDict({1: 2})[1] == 2
        assert CaselessDict({1: 2, "lower": "UPPER"})["LOWER"] == "UPPER"
        with raises(KeyError):
            CaselessDict()[1]

    def test__hash__(self):
        assert hash(CaselessDict()) == hash(CaselessDict())
        assert hash(CaselessDict({1: 2})) != hash(CaselessDict())
        assert hash(CaselessDict({"lower": "UPPER"})) == hash(CaselessDict({"lower": "UPPER"}))
        assert hash(CaselessDict({"lower": "UPPER"})) == hash(CaselessDict({"LOWER": "UPPER"}))

    def test__iter__(self):
        keyvalues = [(1, 2), (3, 4)]
        mapping = CaselessDict(keyvalues)
        for (actual_key, expected_key) in zip(mapping, dict(keyvalues).keys()):
            assert actual_key == expected_key

    def test__len__(self):
        assert len(CaselessDict()) == 0
        assert len(CaselessDict({1: 2})) == 1
        assert len(CaselessDict({1: 2, 3: 4})) == 2

    def test__nonzero__(self):
        assert not bool(CaselessDict())
        assert bool(CaselessDict({1: 2}))
        assert bool(CaselessDict({1: 2, 3: 4}))

    def test__reduce__(self):
        mapping = CaselessDict({1: 2, 3: 4, "hello": "hi"})
        assert round_trip_pickle(mapping) == mapping

    def test__repr__(self):
        assert repr(CaselessDict()) == "CaselessDict({})"
        assert repr(CaselessDict({1: 2})) == "CaselessDict({1: 2})"
        assert repr(CaselessDict({1: 2, 3: 4})) == "CaselessDict({1: 2, 3: 4})"

    def test__sizeof__(self):
        assert getsizeof(CaselessDict()) <= getsizeof(CaselessDict({1: 2, 3: 4}))

    def test__str__(self):
        assert str(CaselessDict()) == "CaselessDict({})"
        assert str(CaselessDict({1: 2})) == "CaselessDict({1: 2})"
        assert str(CaselessDict({1: 2, 3: 4})) == "CaselessDict({1: 2, 3: 4})"

    def test_fromkeys(self):
        assert CaselessDict.fromkeys([1, 2, 3], default=3) == CaselessDict({1: 3, 2: 3, 3: 3})
        assert CaselessDict.fromkeys([1, 2, 3], default=None) == CaselessDict(
            {1: None, 2: None, 3: None}
        )

    def test_copy(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping == mapping.copy()
        updated = CaselessDict({2: 3, 4: 10, "lower": "UPPER"})
        assert updated == mapping.copy({4: 10})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, "lower": "UPPER"})
        assert updated == mapping.copy({6: 7})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, 8: 9, "lower": "UPPER"})
        assert updated == mapping.copy({6: 7, 8: 9})
        updated = CaselessDict({2: 3, 4: 5, 6: 7, 8: 9, "lower": "UPDATED"})
        assert updated == mapping.copy({6: 7, 8: 9, "LOWER": "UPDATED"})

    def test_get(self):
        assert CaselessDict({1: 2}).get(1) == 2
        assert CaselessDict().get(1) is None
        assert CaselessDict().get(1, default=2) == 2
        assert CaselessDict({"lower": "UPPER"}).get("LOWER") == "UPPER"

    def test_items(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).items()) == keyvalues

    def test_keys(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).keys()) == list(dict(keyvalues).keys())

    def test_updated(self):
        mapping = CaselessDict({2: 3, 4: 5, "lower": "UPPER"})
        assert mapping.updated(4, 10) == CaselessDict({2: 3, 4: 10, "lower": "UPPER"})
        assert mapping.updated(6, 7) == CaselessDict({2: 3, 4: 5, 6: 7, "lower": "UPPER"})
        assert mapping.updated("LOWER", "UPDATED") == CaselessDict(
            {2: 3, 4: 5, "lower": "UPDATED"}
        )

    def test_values(self):
        keyvalues = [(1, 2), (3, 4)]
        assert list(CaselessDict(keyvalues).values()) == list(dict(keyvalues).values())
