ifconfig wlan1 10.0.0.1 netmask 255.255.255.0
ifconfig wlan1 mtu 1500
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1
dhcpd -d -f -cf /etc/dhcp/dhcpd.conf wlan1 
