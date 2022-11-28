"""A python ansible runner"""
from pathlib import Path

from ansible import context
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook import Playbook
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager


class DefaultImmutableDict(ImmutableDict):
    """A Immutable dict that returns None for missing keys"""

    def get(self, key, default=None):
        try:
            return self._store[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        try:
            return self._store[key]
        except KeyError:
            return None


class Anirunner:
    def __init__(self) -> None:
        self._base_cliargs = {"verbosity": 0, "check": False, "diff": False}
        self._loader = DataLoader()
        self._passwords = dict(vault_pass="secret")
        self._results_callback = CallbackBase()
        self._inventory = InventoryManager(loader=self._loader, sources=None)
        self._variable_manager = VariableManager(
            loader=self._loader, inventory=self._inventory
        )

    def load_playbook(self, file: Path):
        context.CLIARGS = DefaultImmutableDict(self._base_cliargs)
        loaded_pbook = Playbook.load(
            file, variable_manager=self._variable_manager, loader=self._loader
        )
        context.CLIARGS = ImmutableDict()
        return loaded_pbook

    def syntax_check(self, file: Path):
        context.CLIARGS = DefaultImmutableDict(self._base_cliargs | {"syntax": True})
        playbook_exec = PlaybookExecutor(
            playbooks=[file],
            inventory=self._inventory,
            variable_manager=self._variable_manager,
            loader=self._loader,
            passwords=self._passwords,
        )
        playbook_exec.run()
        context.CLIARGS = ImmutableDict()

    def run(self, file: Path):
        context.CLIARGS = DefaultImmutableDict(self._base_cliargs)
        playbook_exec = PlaybookExecutor(
            playbooks=[file],
            inventory=self._inventory,
            variable_manager=self._variable_manager,
            loader=self._loader,
            passwords=self._passwords,
        )
        playbook_exec.run()
        context.CLIARGS = ImmutableDict()
