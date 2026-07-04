import json

import yaml

from .base import TransformerBot


class Bumblebee(TransformerBot):
    """Bumblebee scouts ahead, translating between JSON and YAML."""

    name = "Bumblebee"

    @property
    def conversions(self):
        return {("json", "yaml"), ("yaml", "json")}

    def transform(self, content: str, from_format: str, to_format: str) -> str:
        if from_format == "json" and to_format == "yaml":
            data = json.loads(content)
            return yaml.dump(data, sort_keys=False)
        if from_format == "yaml" and to_format == "json":
            data = yaml.safe_load(content)
            return json.dumps(data, indent=2) + "\n"
        raise ValueError(f"Bumblebee cannot transform {from_format} -> {to_format}")
