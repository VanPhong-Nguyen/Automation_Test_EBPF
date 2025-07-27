import subprocess
import pytest
import os
import shutil
import shlex


def load_exec_test_cases():
    test_cases = []
    inside_exec = False

    with open("test_case/test_cases.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                inside_exec = line.lower().startswith("# exec")
                continue
            if not inside_exec or not line:
                continue
            test_cases.append(line)
    return test_cases

def should_be_blocked(cmd):
    parts = cmd.split()
    executable = parts[0]
    return executable.startswith("/tmp")


def execute_command(cmd):
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True, timeout=2)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

@pytest.fixture(autouse=True)
def check_executable_exists(request):
    if not hasattr(request.node, "callspec"):
        return

    cmd = request.node.callspec.params.get("cmd")
    if not cmd:
        return

    parts = shlex.split(cmd)
    executable = parts[0]

    if executable.startswith("/") or executable.startswith("."):
        if not os.path.exists(executable):
            pytest.skip(f"Lệnh '{cmd}' bị skip vì file thực thi '{executable}' không exist")
    else:
        if shutil.which(executable) is None:
            pytest.skip(f"Lệnh '{cmd}' bị skip vì lệnh '{executable}' không có trong PATH")

    if executable in ["cat", "bash", "sh"]:
        for part in parts[1:]:
            if part.startswith("/") and not os.path.exists(part):
                pytest.skip(f"Lệnh '{cmd}' bị skip vì file '{part}' không exist")



@pytest.mark.parametrize("cmd", load_exec_test_cases())
def test_exec_blocking(cmd):
    allowed = not should_be_blocked(cmd)
    result = execute_command(cmd)
    assert result == allowed, f"Lệnh '{cmd}' {'nên chạy được' if allowed else 'phải bị chặn'}"
