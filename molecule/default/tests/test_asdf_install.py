# molecule/default/tests/test_asdf_binary.py
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

asdf_binary = vars["asdf_binary"]
asdf_user = vars["asdf_user"]

asdf_config_file = f"/home/{asdf_user}/.asdfrc"


def test_asdf_binary_exists(host):
    bin_file = host.file(asdf_binary)
    assert bin_file.exists
    assert bin_file.is_file
    assert bin_file.mode & 0o111


def test_asdfrc_exists(host):
    """Verify that the .asdfrc file exists, is a file, and has correct ownership and mode."""
    f = host.file(asdf_config_file)

    assert f.exists, f"{asdf_config_file} does not exist"
    assert f.is_file, f"{asdf_config_file} is not a regular file"
    assert f.user == asdf_user, f"{asdf_config_file} is not owned by {asdf_user}"
    assert f.group == asdf_user, f"{asdf_config_file} group is not {asdf_user}"
    assert f.mode == 0o644, f"{asdf_config_file} mode is not 0644"
