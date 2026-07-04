import re

from .base import TransformerBot


class Ratchet(TransformerBot):
    """Ratchet patches up plain Markdown into fully-formed HTML."""

    name = "Ratchet"

    @property
    def conversions(self):
        return {("markdown", "html")}

    def transform(self, content: str, from_format: str, to_format: str) -> str:
        if (from_format, to_format) != ("markdown", "html"):
            raise ValueError(f"Ratchet cannot transform {from_format} -> {to_format}")
        return _markdown_to_html(content)


def _inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def _markdown_to_html(content: str) -> str:
    html = []
    paragraph = []
    list_open = False

    def flush_paragraph():
        if paragraph:
            html.append(f"<p>{_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list():
        nonlocal list_open
        if list_open:
            html.append("</ul>")
            list_open = False

    for line in content.splitlines():
        stripped = line.strip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        list_item = re.match(r"^[-*]\s+(.*)$", stripped)

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            html.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue

        if list_item:
            flush_paragraph()
            if not list_open:
                html.append("<ul>")
                list_open = True
            html.append(f"<li>{_inline(list_item.group(1))}</li>")
            continue

        close_list()
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return "\n".join(html) + "\n"
