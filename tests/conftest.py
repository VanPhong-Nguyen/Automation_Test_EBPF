import pytest
import subprocess
import os
import time

@pytest.fixture(scope="session", autouse=True)
def check_loader():
    """Run the loader before all test cases. If it fails, stop all tests."""
    loader_path = "../ebpf_lsm/loader"

    if not os.path.isfile(loader_path) or not os.access(loader_path, os.X_OK):
        pytest.exit(f"❌ Loader path invalid or not executable: {loader_path}", returncode=1)

    print(f"[INFO] Starting loader in background: {loader_path}")

    try:
        # Chạy loader ở background
        loader_proc = subprocess.Popen([loader_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # đợi policy được gắn

        # --- CHẠY fake_exec.sh ở đây ---
        fake_exec_path = os.path.join(os.path.dirname(__file__), "test_case", "simulate_backend", "fake_exec.sh")

        if not os.path.isfile(fake_exec_path):
            pytest.exit(f"❌ Không tìm thấy fake_exec.sh tại {fake_exec_path}", returncode=1)

        if not os.access(fake_exec_path, os.X_OK):
            os.chmod(fake_exec_path, 0o755)

        print(f"[INFO] Thực thi fake_exec.sh: {fake_exec_path}")
        result = subprocess.run(["bash", fake_exec_path], capture_output=True, text=True)

        print("[DEBUG] fake_exec.sh output:")
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            pytest.exit("❌ Lỗi khi chạy fake_exec.sh", returncode=1)
        # --- END fake_exec.sh ---

        yield  # cho phép test chạy

    finally:
        print("[INFO] Stopping loader after test session.")
        loader_proc.terminate()
        loader_proc.wait()
