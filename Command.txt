# Network-PJ6-CDN

## Command to login to http server 
ssh -i ssh-ed25519-wu.hsin.priv wu.hsin@cdn-http3.khoury.northeastern.edu


### ipvs addr: 

cdn-http3: 45.33.55.171
cdn-http4: 170.187.142.220
cdn-http7: 213.168.249.157
cdn-http11: 139.162.82.207
cdn-http14: 45.79.124.209
cdn-http15: 192.53.123.145
cdn-http16: 192.46.221.203

### To deploy 
./deployCDN.sh -p 20260 -o http://cs5700cdnorigin.ccs.neu.edu:8080/. -n cs5700cdn.example.com. -u wu.hsin -i /Users/ianwu/Desktop/NEU/CS5700_NETWORK/ssh-ed25519-wu.hsin.priv 

### To Run 
./runCDN.sh -p 20260 -o http://cs5700cdnorigin.ccs.neu.edu:8080/. -n cs5700cdn.example.com. -u wu.hsin -i /Users/ianwu/Desktop/NEU/CS5700_NETWORK/ssh-ed25519-wu.hsin.priv 

### To Stop
./stopCDN.sh -p 20260 -o http://cs5700cdnorigin.ccs.neu.edu:8080/. -n cs5700cdn.example.com. -u wu.hsin -i /Users/ianwu/Desktop/NEU/CS5700_NETWORK/ssh-ed25519-wu.hsin.priv 

