from mitmproxy import http
import time, re

def response(flow: http.HTTPFlow) -> None:
    desired_speed_bytes_ps = 1e6  # Adjust this to your desired bytes per second
    if flow.response:
        delay = len(flow.response.content) / desired_speed_bytes_ps
        time.sleep(delay)


