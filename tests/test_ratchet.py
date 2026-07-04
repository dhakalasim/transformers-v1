import pytest

from transformers_v1.bots.ratchet import Ratchet


def test_markdown_to_html_headings_and_lists():
    bot = Ratchet()
    md = "# Title\n\nSome **bold** and *italic* text.\n\n- one\n- two\n"
    html = bot.transform(md, "markdown", "html")
    assert "<h1>Title</h1>" in html
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<ul>" in html and "<li>one</li>" in html


def test_unsupported_pair_raises():
    bot = Ratchet()
    with pytest.raises(ValueError):
        bot.transform("x", "html", "markdown")
