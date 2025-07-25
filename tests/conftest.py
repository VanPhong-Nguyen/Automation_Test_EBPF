import pytest
import subprocess
import os
import time

@pytest.fixture(scope="session", autouse=True)
def check_loader():
    """Run the loader before all test cases. If it fails, stop all tests."""
    loader_path = "/home/caukimam/project_Ebpf_lsm/ebpf_lsm/loader"

    if not os.path.isfile(loader_path) or not os.access(loader_path, os.X_OK):
        pytest.exit(f"❌ Loader path invalid or not executable: {loader_path}", returncode=1)

    print(f"[INFO] Starting loader in background: {loader_path}")

    try:
        # Chạy loader ở background
        loader_proc = subprocess.Popen([loader_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # đợi policy được gắn

        yield  # cho phép test chạy

    finally:
        print("[INFO] Stopping loader after test session.")
        loader_proc.terminate()
        loader_proc.wait()
