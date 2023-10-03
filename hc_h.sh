#!/bin/bash

show_logo(){
    base64 -d <<<"H4sIAAAAAAAAA52R3Q2AMAiE3zvFDWBkAUcxOQdxeIH+iPBmm34px9GSFgBI1FHELLxxyJSqpksg
tFQHHTRxCFxCcE3Dt97Fj62ZqNGpdBCXE0vgQnDZ+aJAqi+2Zpf6RG/KA77C6Cq5FNuB2X/IpFp9
IunHnnabYgtkb3HugsvimzdTRrd7cKw/+DlkfEVUpLjaAwdz98xGAgAA" | gunzip
}

check_headers() {
    local url="$1"
    local show_all_headers="$2"
    local headers=("Strict-Transport-Security" "Content-Security-Policy")
    local curl_headers=(
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        "Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        "Accept-Encoding: gzip, deflate"
        "Cache-Control: max-age=0"
        "Connection: keep-alive"
    )
    
    local response
    local status_code
    local response_reason
    local status_line
    
    echo -e "\nAnalyzing $url:\n"
    response=$(curl -I -s -L -H "${curl_headers[@]}" "$url")
    
    # Check if the response is empty
    if [[ -z "$response" ]]; then
        echo -e "\e[31m" "\nNo response from $url" "\e[0m"
        echo -e "\n========================================\n"
        return
    fi
    
    status_line=$(echo "$response" | grep "^HTTP")
    status_code=$(echo "$status_line" | awk '{print $2}')
    response_reason=$(echo "$status_line" | awk '{$1=""; print}' | sed 's/^[ \t]*//')
    
    echo -e "$response_reason"
    specific_headers=("Server" "Via" "X-Powered-By" "X-AspNet-Version", "http-server-header")
    for header in "${specific_headers[@]}"; do
        value=$(grep -i "^$header:" <<< "$response" | awk '{ $1=""; print }' | sed 's/^[ \t]*//')
        if [[ -n "$value" ]]; then
            echo "$(tput setaf 5)$header: $value$(tput sgr0)"
        fi
    done
    
    if [[ "$show_all_headers" = true ]]; then
        echo -e "\nAll Response Headers:"
        echo "$response"
    fi
    
    if ! grep -iq "^Strict-Transport-Security:" <<< "$response"; then
        echo -e "$(tput setaf 5)Missing Strict-Transport-Security header $(tput sgr0)"
    fi
    if ! grep -iq "^Content-Security-Policy:" <<< "$response"; then
        echo -e "$(tput setaf 5)Missing Content-Security-Policy header $(tput sgr0)"
    fi
    
    echo -e "\n\n========================================\n"
}

# Main code
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <url_or_file>"
    echo "    -h    show all response headers"
    exit 1
fi

target="$1"
show_all_headers=false
show_logo

if [[ "$2" = "-h" ]]; then
    show_all_headers=true
fi

if [[ -f "$target" ]]; then
    while IFS= read -r url; do
        check_headers "$url" "$show_all_headers"
    done < "$target"
else
    check_headers "$target" "$show_all_headers"
fi
