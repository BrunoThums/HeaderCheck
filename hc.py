#!/usr/bin/python
import sys # Used to read arguments
import requests # Used to HTTP requestes
import urllib3 # Control SSL warn messages
import subprocess
from termcolor import colored # Add color to text
from urllib.parse import urlsplit, urlunsplit # Functions to work with URL

# Function to colorize the response code and reason
def get_colored_response_status(status_code, status_code_reason):
    colors = {
        "1xx": "blue",
        "2xx": "green",
        "3xx": "cyan",
        "4xx": "yellow",
        "5xx": "red",
        "other": "white"
    }
    
    if 100 <= status_code < 200:
        category = "1xx"
    elif 200 <= status_code < 300:
        category = "2xx"
    elif 300 <= status_code < 400:
        category = "3xx"
    elif 400 <= status_code < 500:
        category = "4xx"
    elif 500 <= status_code < 600:
        category = "5xx"
    else:
        category = "other"
    
    color = colors[category]
    colored_status = colored(str(status_code), color)
    colored_reason = colored(status_code_reason, color)
    
    return f"{colored_status} {colored_reason}"

# Function used to add https:// at the beginning of the URL and remove the subdirectories
def normalize_url(url, use_ports_80_443=True):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    elif url.startswith("http://"):
        url = "https://" + url[7:]  # Remove "http://" and replace with "https://"
    url_parts = urlsplit(url)
    # Check if was passed the parameter --no-ports and if the URL contains any port (url_parts.port detects it)
    # If the parameter wasn't passed and don't have any ports in the URL, add the ports 80 and 443 at the end of it
    if use_ports_80_443 and not url_parts.port:
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
    return url

def check_headers(url, show_all_headers=False, show_report=True, debug=False, show_instant_errors=False):
        # Disable warning for TLS < 1.2
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        divisor = "\n"+("="*40)+"\n"
        # found_header
        f_h = []
        # missed_header
        m_h = []
        # normal_header
        n_h = []
        try:
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
            

            found_header = None
            normal_header = None
            missed_header = None
            if show_instant_errors: print("\nAnalyzing", colored(f"{url}", "light_yellow"),": \n")
            response = session.get(url, headers=headers, timeout=5, verify=False)
            if show_instant_errors: 
                colored_response_status = get_colored_response_status(response.status_code, response.reason)
                print(colored_response_status)
            for header, value in response.headers.items():
                if show_all_headers:
                    if header in specific_headers:
                        found_header = f"{header}: {value}"
                        f_h.append(found_header)
                        if show_instant_errors: print(colored(found_header, "magenta"))
                    else:
                        normal_header = f"{header}: {value}"
                        n_h.append(normal_header)
                        if show_instant_errors: print(colored(normal_header, "white"))
                else:
                    if header in specific_headers:
                        found_header = f"{header}: {value}"
                        f_h.append(found_header)
                        if show_instant_errors: print(colored(found_header, "magenta"))
            # if
            if show_report:
                missing_headers = []
                for header in ["Strict-Transport-Security", "Content-Security-Policy"]:
                    if header not in response.headers:
                        missing_headers.append(header)
                if missing_headers:
                    for missing_header in missing_headers:
                        missed_header = f"Missing {missing_header} header"
                        m_h.append(missed_header)
                        if show_instant_errors: print(colored(missed_header, "magenta"))
            # print exclusively for show_instant_errors
            if (found_header or missed_header) and not show_instant_errors:
                print("\nAnalyzing", colored(f"{url}", "light_yellow"),": \n")
                colored_response_status = get_colored_response_status(response.status_code, response.reason)
                print(colored_response_status)
                if n_h and show_all_headers:
                    for header in n_h: print(colored(header, "white"))
                if f_h:
                    for header in f_h: print(colored(header, "magenta"))
                if m_h:
                    for header in m_h: print(colored(header, "magenta"))
                print(divisor)
            if show_instant_errors: print(divisor)
        
        except KeyboardInterrupt:
            print("\nScript interrupted by user.")
            sys.exit(1)
        #except requests.exceptions.RequestException as e:
        #    print(colored(f"An error occurred: {e}", "red"))
        except requests.exceptions.SSLError as ssl_error: 
            if debug:
                print(colored(f"SSL Error: {ssl_error}", "red"))
                print(divisor)
            elif not show_instant_errors:
                pass
            else:
                print(colored(f"SSL Error", "red"))
                print(divisor)
            url_sslerror.append(url)
        except requests.exceptions.ReadTimeout as read_timeout:
            if debug:
                print(colored(f"Read Timeout: {read_timeout}", "red"))
                print(divisor)
            elif not show_instant_errors:
                pass
            else:
                print(colored(f"Read Timeout", "red"))
                print(divisor)
            urls_with_timeout.append(url)
        except requests.exceptions.ConnectionError as connection_error: 
            if debug:
                print(colored(f"Connection Error: {connection_error}", "red"))
                print(divisor)
            elif not show_instant_errors:
                pass
            else:
                print(colored(f"Connection Error", "red"))
                print(divisor)
            url_connection_error.append(url)
def show_logo():                                                                                                      
    print("    __                   __               __              __    ")
    print("   / /_  ___  ____ _____/ /__  __________/ /_  ___  _____/ /__  ")
    print("  / __ \/ _ \/ __ `/ __  / _ \/ ___/ ___/ __ \/ _ \/ ___/ //_/  ")
    print(" / / / /  __/ /_/ / /_/ /  __/ /  / /__/ / / /  __/ /__/ ,<     ")
    print("/_/ /_/\___/\__,_/\__,_/\___/_/   \___/_/ /_/\___/\___/_/|_|    ")

if __name__ == "__main__":
    urls_with_timeout = []  # Initialize the list to store URLs with timeout
    url_sslerror = []
    url_connection_error = []

    # Define some request headers to bypass (a little) tools/systems/solutions anti-bot
    if len(sys.argv) < 2:
        print("Usage: python script.py <url_or_file>")
        print(colored("--all-headers -h ", "green", attrs=['bold']),end="")
        print("-> show all response headers")
        print(colored("--no-ports -np ", "green", attrs=['bold']),end="")
        print("-> don't add ports 80 and 443. Go all https (443)")
        print(colored("--no-csp-hsts -nr ", "green", attrs=['bold']),end="red")
        print("-> don't verify CSP or HTST")
        print(colored("--debug -d ", "green", attrs=['bold']),end="")
        print("-> show detailed errors")
        print(colored("--show-instant-errors -si ", "green", attrs=['bold']),end="")
        print("-> don't show, at the end, the urls with connection errors. Shows at the instant")
        print("\n", colored("All parameters are", "light_grey"), colored("false", "light_red"), colored("by default", "light_grey"))
        sys.exit(1)
    
    # Initialization definitions
    target = sys.argv[1]
    # False by default
    show_all_headers = "--all-headers" in sys.argv or "-h" in sys.argv
    # True by default
    use_ports_80_443 = not ("--no-ports" in sys.argv or "-np" in sys.argv)
    # True by default
    show_report = not ("--no-csp-hsts" in sys.argv or "-nc" in sys.argv)
    # False by default
    debug = "--debug" in sys.argv or "-d" in sys.argv
    # True by default
    show_instant_errors = "--show-instant-errors" in sys.argv or "-si" in sys.argv
    
    specific_headers = ["Server", "Via", "X-Powered-By", "X-AspNet-Version", "Host"]
    show_logo()
    
    try:
        # read the content of the file
        with open(target, "r") as f:
            # split the content into lines that became the elements of a list (target_urls)
            target_urls = f.read().splitlines()
            # send each URL to normalize_url, adding https:// at the beginning and add, if parameter use_ports equals true, the ports 80 and 443
            target_urls = [normalize_url(url, use_ports_80_443) for url in target_urls]
            # if the use_ports equals true, then we get back two URLs. If is this case, then combine every sublist into a single list
            if use_ports_80_443:
                target_urls = [item for sublist in target_urls for item in sublist]
            # Remove duplicates while preserving order (create a dictionary to remove duplicates and convert it back to a list)
            target_urls = list(dict.fromkeys(target_urls))  
    except FileNotFoundError:
        target_urls = [normalize_url(target, use_ports_80_443)]
        if use_ports_80_443:
            target_urls = [item for sublist in target_urls for item in sublist]
            
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }
    for target_url in target_urls:
        check_headers(target_url, show_all_headers, show_report, debug, show_instant_errors)
        #print("="*40)  # Separate output for each URL
    #if urls_with_timeout:
        #for target_url in urls_with_timeout:
            #check_headers_curl(target_url, show_all_headers, show_report)
    if not show_instant_errors:
        if urls_with_timeout:
            print(colored("URLs with timeout:", "red"))
            for url in urls_with_timeout:
                print(url)
        if url_sslerror:
            print(colored("URLs with SSL error:", "red"))
            for url in url_sslerror:
                print(url)
        if url_connection_error:
            print(colored("URLs with connection error:", "red"))
            for url in url_connection_error:
                print(url)
