#!/bin/bash

# Scripts will be executed as: $ ./deployCDN [-p port] [-o origin] [-n name] [-u username] [-i keyfile]

# Define parameters
DNS_SERVER="cdn-dns.khoury.northeastern.edu"
PORT=""
ORIGIN=""
NAME=""
USER_NAME=""
SSH_KEY=""

# Parse command-line options
while getopts "p:o:n:u:i:" opt; do
  case $opt in
    p) PORT=$OPTARG ;;
    o) ORIGIN=$OPTARG ;;
    n) NAME=$OPTARG ;;
    u) USER_NAME=$OPTARG ;;
    i) SSH_KEY=$OPTARG ;;
    *) echo "Usage: $0 [-p port] [-o origin] [-n name] [-u username] [-i keyfile]" >&2
       exit 1 ;;
  esac
done

# Check required variables
if [[ -z "$USER_NAME" ]] || [[ -z "$SSH_KEY" ]]; then
    echo "Username and keyfile must be provided."
    exit 1
fi

# Start running DNS server 
echo "Start Running DNS Server on $DNS_SERVER"
ssh -i "$SSH_KEY" "$USER_NAME@$DNS_SERVER" << EOF
lsof -ti:$PORT | xargs -r kill

echo "DNS server stop running."
EOF

# Define the server list to delpoy to 
SERVERS=(
    "cdn-http3.khoury.northeastern.edu"
    "cdn-http4.khoury.northeastern.edu"
    "cdn-http7.khoury.northeastern.edu"
    "cdn-http11.khoury.northeastern.edu"
    "cdn-http14.khoury.northeastern.edu"
    "cdn-http15.khoury.northeastern.edu"
    "cdn-http16.khoury.northeastern.edu"
)

# Loop through each server and run the http server
for server in "${SERVERS[@]}"; do

    # SSH into the server, make the script executable, and run it
    ssh -T "$USER_NAME@$server" << EOF
    lsof -ti:$PORT | xargs -r kill
EOF
done

echo "CDN stopped."
