ifconfig wlan0 up 
airmon-ng check kill
airmon-ng start wlan0 
airodump-ng wlan0mon 
airmon-ng stop wlan0mon
