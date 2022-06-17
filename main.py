import speedtest
s = speedtest.Speedtest()

print("Test Download Speed...")

download_result = s.download()/1025/1024
print(f"Your download speed is:{download_result:.2f}mbit/s")

print("Test Upload Speed...")

upload_result = s.upload()/1024/1024
print(f"Your upload speed is:{upload_result:.2f}mbit/s")

print("Test Ping Test...")

ping_result = s.result.ping
print(f"Your ping is:{ping_result}ms")
