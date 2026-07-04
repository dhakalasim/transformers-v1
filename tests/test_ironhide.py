import json

import pytest

from transformers_v1.bots.ironhide import Ironhide


def test_csv_to_json():
    bot = Ironhide()
    result = bot.transform("name,age\nBumblebee,10000\n", "csv", "json")
    assert json.loads(result) == [{"name": "Bumblebee", "age": "10000"}]


def test_json_to_csv():
    bot = Ironhide()
    result = bot.transform(json.dumps([{"name": "Jazz", "age": "9000"}]), "json", "csv")
    assert "name,age" in result
    assert "Jazz,9000" in result


def test_json_object_to_csv_treated_as_single_row():
    bot = Ironhide()
    result = bot.transform(json.dumps({"name": "Optimus Prime", "role": "Leader"}), "json", "csv")
    assert "name,role" in result
    assert "Optimus Prime,Leader" in result


def test_unsupported_pair_raises():
    bot = Ironhide()
    with pytest.raises(ValueError):
        bot.transform("x", "csv", "yaml")
