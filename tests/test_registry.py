import pytest

from transformers_v1.registry import NoAutobotAvailable, OptimusPrime


def test_detect_format_by_extension():
    prime = OptimusPrime()
    assert prime.detect_format("data.json") == "json"
    assert prime.detect_format("data.yaml") == "yaml"
    assert prime.detect_format("notes.md") == "markdown"


def test_find_bot_success():
    prime = OptimusPrime()
    assert prime.find_bot("json", "yaml").name == "Bumblebee"


def test_find_bot_failure_raises():
    prime = OptimusPrime()
    with pytest.raises(NoAutobotAvailable):
        prime.find_bot("html", "csv")


def test_transform_end_to_end():
    prime = OptimusPrime()
    assert "a: 1" in prime.transform('{"a": 1}', "json", "yaml")
