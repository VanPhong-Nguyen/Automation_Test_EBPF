#!/bin/bash

# Tạo 2 tiến trình giả: 1 PID nhỏ (system-like), 1 PID lớn (user-like)
# Ghi PID vào file tạm để test_case.txt đọc

#!/bin/bash

mkdir -p tmp_pid
echo "[+] Creating test processes..."

# PID nhỏ
sleep 60 &
PID_SMALL=$!
disown
echo $PID_SMALL > tmp_pid/pid_small.txt
echo "[+] Created small PID: $PID_SMALL"

# Tăng PID và tạo PID lớn
for i in {1..30}; do sleep 1 & disown; done
sleep 60 &
PID_LARGE=$!
disown
echo $PID_LARGE > tmp_pid/pid_large.txt
echo "[+] Created large PID: $PID_LARGE"

# Đợi 2 giây đảm bảo PID có mặt
sleep 2
exit 0

