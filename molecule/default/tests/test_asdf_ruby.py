# molecule/default/tests/test_asdf_ruby.py

import pytest
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

system_packages = vars.get("asdf_ruby_dependencies", [])


@pytest.mark.parametrize("pkg", system_packages)
def test_system_package_installed(host, pkg):
    """Ensure each system package is installed on the server."""
    cmd = host.run(f"dpkg -s {pkg}")
    assert cmd.rc == 0
