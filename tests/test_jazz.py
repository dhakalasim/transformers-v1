import pytest

from transformers_v1.bots.jazz import Jazz

SOURCE = '''# top comment
def add(a, b):
    # add two numbers
    return a + b

'''


def test_minify_strips_comments_and_blanks():
    bot = Jazz()
    result = bot.transform(SOURCE, "python", "python-min")
    assert "#" not in result
    assert "def add" in result
    namespace = {}
    exec(compile(result, "<test>", "exec"), namespace)
    assert namespace["add"](2, 3) == 5


def test_prettify_produces_valid_python():
    bot = Jazz()
    result = bot.transform(SOURCE, "python", "python-pretty")
    namespace = {}
    exec(compile(result, "<test>", "exec"), namespace)
    assert namespace["add"](2, 3) == 5


def test_unsupported_source_raises():
    bot = Jazz()
    with pytest.raises(ValueError):
        bot.transform("{}", "json", "python-min")
