import requests
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

#Load a wordlist from a file
def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

#Test RCE for a given domain and payload 
def test_rce(domain, payload, follow_redirects, user_agent, only_200, timeout):
    headers = {'User-Agent': user_agent} if user_agent else {}
    
    try:
        url = f"{domain}/{payload}"
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=follow_redirects)  # Use flag for redirects
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}[200]{Style.RESET_ALL} Potential RCE on {domain} with payload: {payload}")
        elif not only_200:
            if response.status_code in [301, 302]:
                print(f"{Fore.YELLOW}[{response.status_code}]{Style.RESET_ALL} Redirect from {url} to {response.headers.get('Location', 'Unknown')}")
            else:
                print(f"{Fore.RED}[{response.status_code}]{Style.RESET_ALL} {url}")
        
    except requests.exceptions.RequestException as e:
        print(f"{Fore.BLUE}Error with {domain}: {e}{Style.RESET_ALL}")

#Main
def main(domains_file, payloads_file, follow_redirects, user_agent, only_200, timeout):
    domains = load_wordlist(domains_file)
    payloads = load_wordlist(payloads_file)

    for domain in domains:
        for payload in payloads:
            test_rce(domain, payload, follow_redirects, user_agent, only_200, timeout)

#Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='RCE Automator: A tool for testing RCE payloads on multiple domains.\n'
                    'Make sure all targets in your domains list start with http:// or https:// for proper requests.\n'
                    'Made by Oscar - github.com/radnovaxwavez',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('domains', help='Path to the domains file (domains.txt). Each domain should start with http:// or https://')
    parser.add_argument('payloads', help='Path to the payloads file (payloads.txt)')
    parser.add_argument('--follow-redirects', action='store_true', help='Follow redirects (default: False)')
    parser.add_argument('--user-agent', help='Custom User-Agent string to send in requests')
    parser.add_argument('--only-200', action='store_true', help='Only display responses with status code 200')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout for each request in seconds (default: 10)')
    
    args = parser.parse_args()

    #Pass flags and arguments to main function
    main(args.domains, args.payloads, args.follow_redirects, args.user_agent, args.only_200, args.timeout)
