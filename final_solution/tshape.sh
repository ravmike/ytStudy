#!/bin/bash

# Reset dummynet to default config
dnctl -f flush

# Compose an addendum to the default config to create a new anchor
read -d '' -r PF <<EOF
dummynet-anchor "throttle"
anchor "throttle"
EOF

# Reset PF to default config and apply our addendum
(cat /etc/pf.conf && echo "$PF") | pfctl -q -f -

# Configure the new anchor
# cat <<EOF | pfctl -q -a throttle -f -
# no dummynet quick on lo0 all
# dummynet out proto tcp group throttle pipe 1
# dummynet out proto udp group throttle pipe 1
# EOF
echo "dummynet in quick proto tcp from any to any pipe 1" | pfctl -q -a throttle -f -

# Create the dummynet queue - adjust speed as desired
dnctl pipe 1 config bw $1Kbit/s

# Show new configs
printf "\nGlobal pf dummynet anchors:\n"
pfctl -q -s dummynet
printf "\nthrottle anchor config:\n"
pfctl -q -s dummynet -a throttle
printf "\ndummynet config:\n"
dnctl show queue

# Enable PF
pfctl -E
