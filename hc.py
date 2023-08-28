import sys # Used to read arguments
import requests # Used to HTTP requestes
import urllib3 # Control SSL warn messages
from termcolor import colored # Add color to text
from urllib.parse import urlsplit, urlunsplit # Functions to work with URL

# Function used to add https:// at the beginning of the URL and remove the subdirectories
def normalize_url(url, no_ports=True):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    elif url.startswith("http://"):
        url = "https://" + url[7:]  # Remove "http://" and replace with "https://"
    url_parts = urlsplit(url)
    # Check if was passed the parameter --no-ports and if the URL contains any port (url_parts.port detects it)
    # If the parameter wasn't passed and don't have any ports in the URL, add the ports 80 and 443 at the end of it
    if no_ports and not url_parts.port:
        # url_parts explained:
            # scheme -> URL scheme (http ou https)
            # netloc -> pick the domain (then add the port with "+" and ":port")
            # path -> path of aplication (in this case, nothing)
            # query -> query of aplication (in this case, nothing)
            # fragment -> of aplication (in this case, nothing)
        # This 3 last functions (ex.: url_parts.path) can be replaced by "" (cause we don't use none of those).
        # This 3 last fields are required for urlunsplit
        url_80 = urlunsplit((url_parts.scheme, url_parts.netloc + ":80", url_parts.path, url_parts.query, url_parts.fragment))
        url_443 = urlunsplit((url_parts.scheme, url_parts.netloc + ":443", url_parts.path, url_parts.query, url_parts.fragment))
        return [url_80, url_443]

def check_headers(url, show_all_headers=False, no_report=False):
    try:
        # Disable warning for TLS < 1.2
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Define some request headers to bypass (a little) tools/systems/solutions anti-bot 
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "",
            "Upgrade-Insecure-Requests": "1"
        }
        # create a sesssion, capable of reusing TCP connections for many HTTP requests
        session = requests.Session()
        # retry 5 times if HTTP status equal type 500, sleeping 0.2 secs times total of retries (0.2, 0.4, 0.6...)
        # Caution: some HTTP connections will ONLY results in status code 500's. Better not use it
        #retries = requests.packages.urllib3.util.retry.Retry(
        #    total=5,
        #    backoff_factor=0.2,
        #    status_forcelist=[500, 502, 503],
        #)
        # HTTP request adapter, using newly written retry configuration
        #adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        adapter = requests.adapters.HTTPAdapter()

        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(url, headers=headers, timeout=5, verify=False)
        
        print(f"Headers for {url}:\n")
        for header, value in response.headers.items():
            if show_all_headers or header in specific_headers:
                if header in specific_headers:
                    print(colored(f"{header}: {value}", "red"))
                else:
                    print(colored(f"{header}: {value}", "white"))
        # if
        if not no_report:
            missing_headers = []
            for header in ["Strict-Transport-Security", "Content-Security-Policy"]:
                if header not in response.headers:
                    missing_headers.append(header)
            if missing_headers:
                print(colored("Report:", "magenta"))
                print(url)
                for missing_header in missing_headers:
                    print(f"Missing {missing_header} header")
                
        print("="*40)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(1)
    #except requests.exceptions.RequestException as e:
    #    print(colored(f"An error occurred: {e}", "red"))
    except requests.exceptions.SSLError as ssl_error:
        print(colored(f"SSL Error: {ssl_error}", "red"))
    except requests.exceptions.ReadTimeout as read_timeout:
        print(colored(f"Read Timeout: {read_timeout}", "red"))
    except requests.exceptions.ConnectionError as connection_error:
        print(colored(f"Connection Error: {connection_error}", "red"))
    except ConnectionRefusedError:
        print(colored("Connection refused: The server refused the connection.", "red"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <url_or_file>\n--all-headers -H -> show all response headers\n--no-ports -NP -> don't add ports 80 and 443. Go all https (443)\n--no-report -NR -> don't show report at the end")
        sys.exit(1)
    
    target = sys.argv[1]
    show_all_headers = "--all-headers" or "-H" in sys.argv
    no_ports = "--no-ports" or "-NP" not in sys.argv
    no_report = "--no-report" or "-NR" not in sys.argv
    
    specific_headers = ["Server", "Via", "X-Powered-By", "X-AspNet-Version", "Host"]
    
    try:
        with open(target, "r") as f:
            target_urls = f.read().splitlines()
            target_urls = [normalize_url(url, no_ports) for url in target_urls]
            target_urls = [item for sublist in target_urls for item in sublist]  # Flatten the list
            target_urls = list(dict.fromkeys(target_urls))  # Remove duplicates while preserving order
    except FileNotFoundError:
        target_urls = [normalize_url(target, no_ports)]
    
    for target_url in target_urls:
        check_headers(target_url, show_all_headers, no_report)
        print("="*40)  # Separate output for each URL
