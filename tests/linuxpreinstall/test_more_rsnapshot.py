import os
import pytest
from linuxpreinstall.more_rsnapshot import install_files

@pytest.mark.parametrize("target, dst", install_files)
def test_install_files(target, dst):
    assert os.path.isfile(target), f"File {target} does not exist."
