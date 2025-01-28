import json

import pytest
from typer.testing import CliRunner 

from empuje import SUCCESS, __app_name__, __version__, cli, empuje

runner = CliRunner()

# tests/test_rptodo.py
# ...

test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "empuje": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "empuje": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version {__version__}" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    empuje = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "empuje.json"
    with db_file.open("w") as db:
        json.dump(empuje, db, indent=4)
    return db_file


@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["empuje"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["empuje"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    empujer = empuje.Empujer(mock_json_file)
    assert empujer.add(description, priority) == expected
    read = empujer._db_handler.read_empuje()
    assert len(read.empuje_list) == 2
