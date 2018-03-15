#/usr/bin
tshark -i eth0 -l -n -t ad -Y http.request -T fields  -e "frame.time" -e "http.host" -e "ip.src" -e "http.request.uri" -e "http.cookie" -e "eth.src" -e "http.request.full_uri" -e "http.response.code" -e "http.response.phrase" -e "http.content_length" -e "data" -e "text" >> /home/teminal.log

