"""Some tests running a playbook with missing plugins, roles, etc."""
from pathlib import Path

import pytest
from ansible.errors import AnsibleParserError

import anirunner


def test_load_valid_playbook():
    """Demonstrates the running of a valid playbook."""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/valid.yaml")
    runner.run(playbook_file)
    assert True


def test_load_invalid_playbook():
    """Demonstrate the running of an invalid playbook"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/invalid.yaml")
    with pytest.raises(AnsibleParserError) as excinfo:
        runner.run(playbook_file)
    assert "'foo' is not a valid attribute for a Play" in str(excinfo.value)


def test_load_missing_plugin():
    """Demonstrate the running of an playbook with missing plugin"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/missing_plugin.yaml")
    with pytest.raises(AnsibleParserError) as excinfo:
        runner.run(playbook_file)
    assert "couldn't resolve module/action 'collection.missing.plugin'" in str(
        excinfo.value
    )


def test_mock_missing_role(capsys):
    """Demonstrate the running of an playbook with a missing role, no errors"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/missing_role.yaml")
    runner.run(playbook_file)
    captured = capsys.readouterr()
    assert "ERROR! the role 'collection.missing.role' was not found" in captured.err


def test_invalide_jinja(capsys):
    """Demonstrate the running of an playbook with invalid jinja, no errors"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/invalid_jinja.yaml")
    runner.run(playbook_file)
    captured = capsys.readouterr()
    assert "template error while templating string" in captured.out


def test_mock_real_role():
    """Demonstrate the running of an playbook with a real broken role, no errors"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/real_role.yaml")
    with pytest.raises(Exception) as excinfo:
        runner.run(playbook_file)
    assert (
        "The tasks/main.yml file for role 'test' must contain a list of tasks"
        in str(excinfo.value)
    )
