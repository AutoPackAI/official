import os
import sys

import pytest
from autopack.pack_config import PackConfig


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))

    print(f"Executing tests in the directory {tmpdir.strpath}")

    # Set workspace dir for tools
    workspace_path = os.path.join(tmpdir, "workspace")
    os.makedirs(workspace_path, exist_ok=True)
    PackConfig.global_config().workspace_path = workspace_path

    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield

    sys.path.remove(str(tmpdir))
