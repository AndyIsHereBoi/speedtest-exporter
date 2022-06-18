# Speedtest-exporter

This module exports data from speedtest.net, and sends it out to a endpoint for Prometheus to grab.
It will work on anything that can run python 3.6+

# Setup instructions:
`1.` Create a directory at `/etc/speedtest_exporter` using `mkdir /etc/speedtest_exporter`

`2.` Copy the main.py and the requirements.txt file into `/etc/speedtest_exporter`

`3.` Install the required modules by running `pip install -r /etc/speedtest_exporter/requirements.txt`

`4.` Make a service file for your file to keep it online, and start on boot

run `nano /etc/systemd/system/speedtest_exporter.service` and paste the following below:

```
[Unit]
Description=Exports speedtest data to a Prometheus metrics URL to be scraped.
After=network.target

[Service]
Type=simple
User=nobody
Restart=on-failure
RestartSec=5s
ExecStart=python3 /etc/speedtest_exporter/main.py

[Install]
WantedBy=multi-user.target
```

`5.` Run `systemctl enable speedtest_exporter` and `systemctl start speedtest_exporter` to start on boot, and then start speedtest-exporter now.

`6.` Go to http://server_ip:9394/metrics to view your speedtest stats. You can import this into Prometheus via the following config snippet:
  
  ```
  - job_name: speedtest_export
    scrape_interval: 2m
    scrape_timeout: 50s
    static_configs:
      - targets: ["server_ip:9394"]
  ```
  
  You want to keep the scrape interval high, and timeout high. The test may take a minute to run, so you do not want to overload it and then have them building up.
