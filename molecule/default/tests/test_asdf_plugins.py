# molecule/default/tests/test_asdf_plugins.py

import pytest
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

asdf_user = vars["asdf_user"]
asdf_plugins = vars["asdf_plugins"]

plugin_names = [plugin["name"] for plugin in asdf_plugins]

plugin_versions = [
    (plugin["name"], version)
    for plugin in asdf_plugins
    if "install" in plugin
    for version in plugin["install"]
]

default_versions = [
    (plugin["name"], plugin.get("default", plugin["install"][0]))
    for plugin in asdf_plugins
    if "install" in plugin and plugin["install"]
]


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
    assert cmd.rc == 0
    installed_plugins = [
        line.strip() for line in cmd.stdout.splitlines() if line.strip()
    ]
    for plugin in plugin_names:
        assert plugin in installed_plugins


@pytest.mark.parametrize("plugin,version", plugin_versions)
def test_install_plugin_version_directories(host, plugin, version):
    """Check if install directory for plugin version exists and is correct"""
    home = host.user(asdf_user).home
    path = f"{home}/.asdf/installs/{plugin}/{version}"
    d = host.file(path)

    assert d.exists
    assert d.is_directory
    assert d.user == asdf_user
    assert d.group == asdf_user


@pytest.mark.parametrize("plugin,version", plugin_versions)
def test_asdf_list_versions(host, plugin, version):
    """Check that the version is listed in `asdf list <plugin>` output"""
    cmd = host.run(f"sudo -u {asdf_user} asdf list {plugin}")
    assert cmd.rc == 0
    installed = [line.strip() for line in cmd.stdout.splitlines() if line.strip()]
    assert any(version in line for line in installed)


@pytest.mark.parametrize("plugin,expected_default", default_versions)
def test_asdf_default_versions(host, plugin, expected_default):
    """
    Verify `asdf current <plugin>` shows the expected default version.
    """
    cmd = host.run(f"sudo -u {asdf_user} asdf current {plugin}")
    assert cmd.rc == 0

    lines = [line for line in cmd.stdout.splitlines() if line.strip()]
    assert len(lines) >= 1

    for line in lines:
        if plugin in line:
            parts = line.split()
            assert expected_default in parts
            break
    else:
        assert False
