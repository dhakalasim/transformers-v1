import ast
import io
import tokenize

from .base import TransformerBot


class Jazz(TransformerBot):
    """Jazz is smooth and stylish -- he keeps Python code looking sharp."""

    name = "Jazz"

    @property
    def conversions(self):
        return {("python", "python-min"), ("python", "python-pretty")}

    def transform(self, content: str, from_format: str, to_format: str) -> str:
        if from_format != "python":
            raise ValueError(f"Jazz cannot transform {from_format} -> {to_format}")
        if to_format == "python-min":
            return _strip_comments_and_blanks(content)
        if to_format == "python-pretty":
            return ast.unparse(ast.parse(content)) + "\n"
        raise ValueError(f"Jazz cannot transform {from_format} -> {to_format}")


def _strip_comments_and_blanks(source: str) -> str:
    tokens = [
        tok
        for tok in tokenize.generate_tokens(io.StringIO(source).readline)
        if tok.type != tokenize.COMMENT
    ]
    stripped = tokenize.untokenize(tokens)
    lines = [line for line in stripped.splitlines() if line.strip()]
    return "\n".join(lines) + "\n"
