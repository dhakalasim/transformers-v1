import json

import pytest

from transformers_v1.bots.bumblebee import Bumblebee


def test_json_to_yaml():
    bot = Bumblebee()
    result = bot.transform('{"a": 1, "b": [1, 2]}', "json", "yaml")
    assert "a: 1" in result
    assert "b:" in result


def test_yaml_to_json():
    bot = Bumblebee()
    result = bot.transform("a: 1\nb:\n  - 1\n  - 2\n", "yaml", "json")
    assert json.loads(result) == {"a": 1, "b": [1, 2]}


def test_unsupported_pair_raises():
    bot = Bumblebee()
    with pytest.raises(ValueError):
        bot.transform("x", "json", "csv")
