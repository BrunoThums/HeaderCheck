#!/bin/bash

echo -e "\033[36m Setup for HeaderCheck commencing! \033[0m"

# Verify if command was used with sudo
if [ "$(id -u)" -ne 0 ]; then
    echo -e "\033[36m Execute again with sudo, please! \033[0m"
    exit 1
fi

# Install required packages
echo -e "\033[36m Installing Python packages... \033[0m"
pip install requests termcolor urllib3
echo -e "\033[36m Installed required Python packages. \033[0m"

wget "https://raw.githubusercontent.com/BrunoThums/HeaderCheck/main/hc.py"
wget "https://raw.githubusercontent.com/BrunoThums/HeaderCheck/main/hc_h.sh"

# Make the SSLVerifier.sh script executable
chmod +x "hc_c.sh"

# Move the entire directory to /usr/local/bin
echo -e "\033[36m Moving script to path \033[0m"
mv hc.py /usr/bin/hc
mv hc_c.sh /usr/bin/hc_c
echo -e "\033[36m Done! \033[0m"
echo -e "\033[36m You can now use headercheck anywhere :) \033[0m"
echo -e "\033[36m Goodbye! \033[0m"

rm setup.sh
