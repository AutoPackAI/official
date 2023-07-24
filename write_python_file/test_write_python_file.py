import os
import sys

import pytest

from write_python_file.write_python_file import WritePythonFile


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))

    print(f"Executing tests in the directory {tmpdir.strpath}")

    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield

    sys.path.remove(str(tmpdir))


def test_write_python_file_success():
    os.makedirs("workspace", exist_ok=True)
    pack = WritePythonFile(workspace_path="workspace")
    code = "print('Hello world!')"
    file_name = "hello_world.py"
    result = pack.run(file_name=file_name, code=code)

    assert result == f"Compiled successfully and saved to hello_world.py."

    with open(os.path.join("workspace", file_name), "r") as f:
        assert f.read() == code


def test_write_python_file_compile_error():
    os.makedirs("workspace", exist_ok=True)
    pack = WritePythonFile(workspace_path="workspace")
    code = "asdf!"
    file_name = "error.py"
    result = pack.run(file_name=file_name, code=code)

    assert "invalid syntax" in result

    assert not os.path.exists(os.path.join("workspace", file_name))
