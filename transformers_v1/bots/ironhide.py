import csv
import io
import json

from .base import TransformerBot


class Ironhide(TransformerBot):
    """Ironhide is built tough for wrangling tabular data."""

    name = "Ironhide"

    @property
    def conversions(self):
        return {("csv", "json"), ("json", "csv")}

    def transform(self, content: str, from_format: str, to_format: str) -> str:
        if from_format == "csv" and to_format == "json":
            rows = list(csv.DictReader(io.StringIO(content)))
            return json.dumps(rows, indent=2) + "\n"
        if from_format == "json" and to_format == "csv":
            data = json.loads(content)
            rows = [data] if isinstance(data, dict) else data
            if not rows:
                return ""
            if not all(isinstance(row, dict) for row in rows):
                raise ValueError("Ironhide needs a JSON object or a list of JSON objects to build a CSV")
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
            return buffer.getvalue()
        raise ValueError(f"Ironhide cannot transform {from_format} -> {to_format}")
