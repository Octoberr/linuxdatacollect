iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE
echo "1" >/proc/sys/net/ipv4/ip_forward
