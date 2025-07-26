import subprocess
import pytest

def run_ping(ip: str) -> bool:
    """Ping IP, trả về True nếu ping thành công."""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def load_network_test_cases():
    test_cases = []
    inside_network = False

    with open("test_case/test_cases.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                inside_network = line.lower().startswith("# network")
                continue
            if not inside_network:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            _, ip = parts
            should_be_blocked = (ip == "1.1.1.1")  # Block rule logic here
            test_cases.append((ip, should_be_blocked))

    return test_cases

@pytest.mark.parametrize("ip,should_be_blocked", load_network_test_cases())
def test_ping_behavior(ip, should_be_blocked):
    result = run_ping(ip)
    if should_be_blocked:
        assert not result, f"[FAIL] {ip} should be blocked but responded"
    else:
        assert result, f"[FAIL] {ip} should be allowed but was blocked"
