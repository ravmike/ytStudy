#!/usr/bin/env bash

dnctl -q flush

pfctl -f /etc/pf.conf
