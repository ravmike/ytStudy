#!/usr/bin/env bash

pfctl -E

(cat /etc/pf.conf && echo "dummynet-anchor \"customRule\"" && echo "echo \"customRule\"") | pfctl -f -

echo "dummynet in quick proto tcp from any to any pipe 1" | pfctl -a customRule -f -

dnctl pipe 1 config bw 500Kbit/s
