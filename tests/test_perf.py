import subprocess
import pytest

def load_perf_test_cases():
    test_cases = []
    inside_perf = False

    with open("test_cases.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                inside_perf = line.lower().startswith("# perf")
                continue
            if not inside_perf or line.startswith("ping") or not line:
                continue
            test_cases.append(line)

    return test_cases

def should_be_blocked(cmd):
    return cmd.startswith("/tmp")

def execute_command(cmd):
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True, timeout=2)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

@pytest.mark.parametrize("cmd", load_perf_test_cases())
def test_perf_exec_blocking(cmd):
    allowed = not should_be_blocked(cmd)
    result = execute_command(cmd)
    assert result == allowed, f"Lệnh '{cmd}' {'nên chạy được' if allowed else 'phải bị chặn'}"
