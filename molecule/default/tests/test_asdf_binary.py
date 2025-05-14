# molecule/default/tests/test_asdf_binary.py
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

asdf_binary = vars["asdf_binary"]


def test_asdf_binary_exists(host):
    bin_file = host.file(asdf_binary)
    assert bin_file.exists
    assert bin_file.is_file
    assert bin_file.mode & 0o111  # is executable
