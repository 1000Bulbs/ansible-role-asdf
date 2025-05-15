# molecule/default/tests/test_asdf_plugins.py

import pytest
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

asdf_user = vars["asdf_user"]
asdf_plugins = vars["asdf_plugins"]

plugins = [plugin["name"] for plugin in asdf_plugins]
plugin_names = [plugin["name"] for plugin in asdf_plugins]


@pytest.mark.parametrize("plugin", plugin_names)
def test_plugin_directory_exists(host, plugin):
    """Verify plugin directory exists and is owned by asdf_user"""
    home = host.user(asdf_user).home
    plugin_path = f"{home}/.asdf/plugins/{plugin}"
    plugin_dir = host.file(plugin_path)

    assert plugin_dir.exists
    assert plugin_dir.is_directory
    assert plugin_dir.user == asdf_user
    assert plugin_dir.group == asdf_user


def test_asdf_plugin_list(host):
    """Verify each plugin is listed in `asdf plugin list` output"""
    cmd = host.run(f"sudo -u {asdf_user} asdf plugin list")
    assert cmd.rc == 0, f"`asdf plugin list` failed for {asdf_user}"
    installed_plugins = [
        line.strip() for line in cmd.stdout.splitlines() if line.strip()
    ]

    for plugin in plugin_names:
        assert plugin in installed_plugins
