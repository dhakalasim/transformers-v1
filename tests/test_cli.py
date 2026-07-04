import json

from transformers_v1.cli import main


def test_transform_json_to_yaml(tmp_path, capsys):
    input_path = tmp_path / "data.json"
    input_path.write_text(json.dumps({"a": 1}))

    exit_code = main(["transform", str(input_path), "--to", "yaml"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Rolling out Bumblebee" in captured.out
    output_path = tmp_path / "data.yaml"
    assert output_path.exists()
    assert "a: 1" in output_path.read_text()


def test_transform_unsupported_pair(tmp_path, capsys):
    input_path = tmp_path / "notes.md"
    input_path.write_text("# hi")

    exit_code = main(["transform", str(input_path), "--to", "csv"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "No Autobot" in captured.out


def test_list_bots(capsys):
    exit_code = main(["list-bots"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Bumblebee" in captured.out
