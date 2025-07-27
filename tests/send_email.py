import yagmail

def send_report():
    receiver = "nguyenvanphong.adapt@gmail.com"
    yag = yagmail.SMTP("nguyenvanphong.adapt@gmail.com", "qpcpdveghyrghcwk")

    with open("test_results.txt", "r") as f:
        content = f.read()

    yag.send(to=receiver, subject="eBPF Test Report", contents=content)

if __name__ == "__main__":
    send_report()
