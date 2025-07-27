import subprocess
import pytest
import os

def run_command(cmd: str) -> str:
    """Chạy lệnh shell và trả về output stderr."""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stderr.decode()

def load_exec_test_cases():
    test_cases = []
    inside_exec = False

    with open("test_case/test_cases.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                inside_exec = line.lower().startswith("# perf")
                continue
            if not inside_exec or not line:
                continue
            test_cases.append(line)
    return test_cases

@pytest.mark.parametrize("cmd", load_exec_test_cases())
def test_perf_access(cmd):
    print(f"Running: {cmd}")
    stderr_output = run_command(cmd)

    if "-p 1500" in cmd:
        assert "Permission denied" in stderr_output or "not allowed" in stderr_output, f"Expected block for: {cmd}"
    else:
        assert "Performance counter stats" in stderr_output or "sleep" in stderr_output or "task-clock" in stderr_output, f"Expected success for: {cmd}"
