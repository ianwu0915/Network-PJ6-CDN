#!/bin/bash

# Scripts will be executed as: $ ./deployCDN [-p port] [-o origin] [-n name] [-u username] [-i keyfile]

# Define parameters
HTTP_SCRIPT_FILE="httpserver"
DNS_SCRIPT_FILE="dnsserver"
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

# Check if the script files exist
if [[ ! -f "$HTTP_SCRIPT_FILE" ]] || [[ ! -f "$DNS_SCRIPT_FILE" ]]; then
    echo "Error: Required script files not found."
    exit 1
fi

# scp dns source code to dns server
DNSERVER="cdn-dns.khoury.northeastern.edu"

scp -i "$SSH_KEY" "$DNS_SCRIPT_FILE" "$USER_NAME@$DNSERVER:~/"
ssh -i "$SSH_KEY" "$USER_NAME@$DNS_SERVER" << EOF
pip install ip2geotools
pip install dnslib
pip install requests
EOF

echo "DNS source code uploaded."


# Define the server list to delpoy to 
SERVERS=(
    "cdn-http3.khoury.northeastern.edu"
    # "cdn-http4.khoury.northeastern.edu"
    # "cdn-http7.khoury.northeastern.edu"
    # "cdn-http11.khoury.northeastern.edu"
    # "cdn-http14.khoury.northeastern.edu"
    # "cdn-http15.khoury.northeastern.edu"
    # "cdn-http16.khoury.northeastern.edu"
)

# Loop through each server and deploy the script
for server in "${SERVERS[@]}"; do
    echo "Deploying to $server"

    # Copy the script to the server
    scp -i "$SSH_KEY" "$HTTP_SCRIPT_FILE" "$USER_NAME@$server:~/"
    echo "Source code uploaded."

done

echo "Deployment completed."
