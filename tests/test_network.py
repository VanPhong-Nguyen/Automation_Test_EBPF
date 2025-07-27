import socket
import pytest
import re

def try_tcp_connect(ip: str, port: int = 443) -> bool:
    """Thử tạo socket kết nối đến IP, trả về True nếu thành công."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        s.close()
        return True
    except (PermissionError, OSError):
        return False

def extract_ip(cmd: str) -> str | None:
    """Rút địa chỉ IP từ câu lệnh giả lập."""
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    match = re.search(ip_pattern, cmd)
    if match:
        return match.group(0)
    return None

def load_network_test_cases():
    test_cases = []
    inside_network = False

    with open("test_case/test_cases.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                inside_network = line.lower().startswith("# network")
                continue
            if not inside_network or not line:
                continue

            ip = extract_ip(line)
            if not ip:
                continue
            should_be_blocked = (ip == "1.1.1.1")  # hoặc mở rộng thêm danh sách IP bị chặn
            test_cases.append((line, ip, should_be_blocked))

    return test_cases

@pytest.mark.parametrize("cmd,ip,should_be_blocked", load_network_test_cases())
def test_command_connect_behavior(cmd, ip, should_be_blocked):
    result = try_tcp_connect(ip)
    if should_be_blocked:
        assert not result, f"[FAIL] `{cmd}` (-> {ip}) should be blocked but connected"
    else:
        assert result, f"[FAIL] `{cmd}` (-> {ip}) should be allowed but was blocked"
