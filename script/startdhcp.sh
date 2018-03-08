ifconfig wlan1 10.0.0.1 netmask 255.255.255.0
ifconfig wlan1 mtu 1500
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1
dhcpd -d -f -cf /etc/dhcp/dhcpd.conf wlan1
iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE
echo "1" > /proc/sys/net/ipv4/ip_forward
