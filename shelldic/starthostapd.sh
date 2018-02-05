rfkill unblock wlan
nmcli radio wifi off
sleep 2
hostapd /etc/hostapd/hostapd.conf &> hostapd.log
