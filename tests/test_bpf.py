import subprocess
import os
import pytest

C_SOURCES = [
    "test_case/test_prog_load_block.c",
    "test_case/test_bpf_block.c",
    # Thêm các file test case khác tại đây
]

EXEC_FILE_TEMPLATE = "./test_bpf_exec_{}"  # Ví dụ: test_bpf_exec_0, test_bpf_exec_

def compile_c_test(c_source, exec_file):
    """Biên dịch file C test cụ thể"""
    compile_cmd = ["gcc", c_source, "-o", exec_file]
    result = subprocess.run(compile_cmd, capture_output=True)
    assert result.returncode == 0, f"[FAIL] Compile error in {c_source}:\n{result.stderr.decode()}"

def run_c_test(exec_file):
    """Chạy chương trình C test cụ thể với quyền sudo"""
    result = subprocess.run(["sudo", exec_file], capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

@pytest.mark.parametrize("index, c_source", list(enumerate(C_SOURCES)))
def test_bpf_cases(index, c_source):
    exec_file = EXEC_FILE_TEMPLATE.format(index)
    compile_c_test(c_source, exec_file)
    
    retcode, stdout, stderr = run_c_test(exec_file)

    print(f"\n[DEBUG] stdout from {c_source}:\n{stdout}\n")

    # Tùy thuộc logic test, có thể match theo tên file
    if "block" in c_source:
        assert retcode == 0, f"{c_source} lỗi: {stderr}"
        assert "failed as expected" in stdout, f"{c_source} sai logic:\n{stdout}"
    elif "pass" in c_source:
        assert retcode == 0, f"{c_source} lỗi: {stderr}"
        assert "succeeded" in stdout, f"{c_source} sai logic:\n{stdout}"
    else:
        pytest.skip(f"Chưa định nghĩa logic kiểm tra cho file: {c_source}")

    # Cleanup sau mỗi test
    if os.path.exists(exec_file):
        os.remove(exec_file)
