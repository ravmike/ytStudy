from mitmproxy import http
import time, re
import logging
import sys

with open("save.txt", "r") as f:
    finish = f.read()

print(finish)

def response(flow: http.HTTPFlow) -> None:
    flow.response.headers["newheader"] = 'foo'
def request(flow: http.HTTPFlow) -> None:
    data = flow.request #save request data
    print(data)
    form = data.query["mime"]
    rng = data.query["range"]
    pixel = data.query["itag"]
    dur = data.query["dur"]
    buffer = data.query["rbuf"]
    clen = data.query["clen"]
    req_s = getattr(flow.request, "timestamp_start")
    req_e = getattr(flow.request, "timestamp_end")
    res_s = getattr(flow.response, "timestamp_start")
    res_e = getattr(flow.response, "timestamp_end")
    data_lst = [form, pixel, dur, rng, buffer, clen, req_s, req_e, res_s, res_e]
    if form != "audio/webm":
        write_to_file(data_lst)
def write_to_file(data):
    with open (finish, "a") as f:
        print(*data, file = f, sep =",")
