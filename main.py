import speedtest # MUST BE THE speedtest-cli module. NOT THE speedtest module
import json
import datetime
from prometheus_client import make_wsgi_app, Gauge
from flask import Flask
from waitress import serve
PORT = 9394

app = Flask("Speedtest-Exporter")  # Create flask app


ping = Gauge('speedtest_ping_ms', 'Speedtest current Ping in ms')
download_speed = Gauge('speedtest_download_mb', 'Speedtest current Download Speed in mb')
upload_speed = Gauge('speedtest_upload_mb', 'Speedtest current Upload speed in mb')

# Cache metrics for how long (seconds)?
cache_seconds = 15
cache_until = datetime.datetime.fromtimestamp(0)


def b_mb(b):
  megabytes=b/1024/1024
  return str(round(megabytes, 2))

def bytes_to_bits(bytes_per_sec):
    return str(bytes_per_sec * 8)


def bits_to_megabits(bits_per_sec):
    megabits = round(bits_per_sec * (10**-6), 2)
    return str(megabits) + "Mbps"


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def runTest():
    s = speedtest.Speedtest()
    s.get_servers([])
    s.download()
    s.upload()
    result = str(s.results)

    try:
        actual_ping = str(round(int(s.results.ping),2))
        download = b_mb(int(s.results.download))
        upload = b_mb(int(s.results.upload))
        return (actual_ping, download, upload)
    except Exception as e:
        import traceback
        print(e, traceback.format_exc())
        return (0, 0, 0)

@app.route("/metrics")
def updateResults():
    global cache_until

    if datetime.datetime.now() > cache_until:
        r_ping, r_download, r_upload = runTest()
        ping.set(r_ping)
        download_speed.set(r_download)
        upload_speed.set(r_upload)

        cache_until = datetime.datetime.now() + datetime.timedelta(seconds=cache_seconds)

    return make_wsgi_app()


@app.route("/")
def mainPage():
    return ("Visit /metrics to view metrics.")


print(f"Starting Speedtest-Exporter on http://localhost:{PORT}")
serve(app, host='0.0.0.0', port=PORT)
