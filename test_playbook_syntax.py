"""Some tests execing a playbook with missing plugins, roles, etc."""
from pathlib import Path
from unittest.mock import patch

import ansible
import pytest
from ansible.errors import AnsibleParserError

import anirunner


def test_load_valid_playbook():
    """Demonstrates the exec of a valid playbook."""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/valid.yaml")
    runner.syntax_check(playbook_file)


def test_load_invalid_playbook():
    """Demonstrate the loading of an invalid playbook"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/invalid.yaml")
    with pytest.raises(AnsibleParserError) as excinfo:
        runner.syntax_check(playbook_file)
    assert "'foo' is not a valid attribute for a Play" in str(excinfo.value)


def test_load_missing_plugin():
    """Demonstrate the loading of an playbook with missing plugin"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/missing_plugin.yaml")
    with pytest.raises(AnsibleParserError) as excinfo:
        runner.syntax_check(playbook_file)
    assert "couldn't resolve module/action 'collection.missing.plugin'" in str(
        excinfo.value
    )


def test_mock_missing_plugin():
    """Demonstrate the loading of an playbook with missing plugin, always return shell"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/missing_plugin.yaml")

    orig_func = ansible.plugins.loader.module_loader.find_plugin_with_context

    def find_plugin_with_context(*_args, **_kwargs):
        plugin_load_context = orig_func("ansible.builtin.shell")
        return plugin_load_context

    with patch.object(
        ansible.plugins.loader.module_loader,
        "find_plugin_with_context",
        find_plugin_with_context,
    ):
        runner.syntax_check(playbook_file)


def test_mock_missing_role():
    """Demonstrate the loading of an playbook with a missing role, no errors"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/missing_role.yaml")
    runner.syntax_check(playbook_file)


def test_invalide_jinja():
    """Demonstrate the loading of an playbook with invalid jinja, no errors"""
    runner = anirunner.Anirunner()
    playbook_file = Path("fixtures/invalid_jinja.yaml")
    runner.syntax_check(playbook_file)
