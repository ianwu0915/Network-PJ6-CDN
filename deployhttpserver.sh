#!/bin/bash

# Define the SSH key and the script file
SSH_KEY="/Users/ianwu/Desktop/NEU/CS5700_NETWORK/Network-PJ6-CDN/ssh-ed25519-wu.hsin.priv"
SCRIPT_FILE="/Users/ianwu/Desktop/NEU/CS5700_NETWORK/Network-PJ6-CDN/httpserver"
USER_NAME="wu.hsin"

# Define the server list to delpoy to 
SERVERS=(
    "cdn-http3.khoury.northeastern.edu"
    "cdn-http4.khoury.northeastern.edu"
    # "cdn-http7.khoury.northeastern.edu"
    # "cdn-http11.khoury.northeastern.edu"
    # "cdn-http14.khoury.northeastern.edu"
    # "cdn-http15.khoury.northeastern.edu"
    # "cdn-http16.khoury.northeastern.edu"
)

PORT="20260"
ORIGIN="http://cs5700cdnorigin.ccs.neu.edu:8080/"

# scp $SCRIPT_FILE $USER_NAME@${SERVER[0]}:~/
# ssh wu.hsin@cdn-http3.khoury.northeastern.edu


# Loop through each server and deploy the script
for server in "${SERVERS[@]}"; do
    echo "Deploying to $server"

    # Copy the script to the server
    scp "$SCRIPT_FILE" "$USER_NAME@$server:~/"

    # SSH into the server, make the script executable, and run it
    ssh -T "$USER_NAME@$server" << EOF
    mkdir cache 
    echo "HTTP server deployed and running in background."

    chmod +x httpserver
    nohup ./httpserver -p 20260 -o http://cs5700cdnorigin.ccs.neu.edu:8080/ >httpserver.log 2>&1 &
EOF
done

echo "Deployment completed."

# to kill the process
# lsof -ti:20260 | xargs -r kill