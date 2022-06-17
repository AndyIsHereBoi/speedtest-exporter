import speedtest # MUST BE THE speedtest-cli module. NOT THE speedtest module
s = speedtest.Speedtest()

def b_mb(b):
  megabytes=b/1024/1024
  return round(megabytes,2)

print("Test Download Speed...")

download_result = b_mb(s.download())
print(f"Your download speed is:{download_result}mbit/s")

print("Test Upload Speed...")

upload_result = b_mb(s.upload())
print(f"Your upload speed is:{upload_result}mbit/s")

print("Test Ping Test...")


s.get_servers([])
print("Ping :", s.results.ping)

print(s.results)
