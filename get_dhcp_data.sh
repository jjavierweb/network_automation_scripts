#!/bin/bash
scp dhcp-sevrer:/etc/dhcp/* /etc/dhcp
scp dhcp-server:/var/lib/dhcp/dhcpd.leases .
dhcpd-pools --config=/etc/dhcp/dhcpd.conf --leases=./dhcpd.leases --format=J --output=./test.json
source venv/bin/activate
python dhcp_analyzer.py
deactivate
