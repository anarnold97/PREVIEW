import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def check_links(target_url):
    print(f"Scanning: {target_url}\n" + "-"*50)
    
    target_domain = urlparse(target_url).netloc

    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code != 200:
            print(f"CRITICAL: Could not access target URL. Status: {response.status_code}")
            return
    except requests.RequestException as e:
        print(f"CRITICAL: Failed to connect to target URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    unique_urls = set()
    for link in links:
        href = link['href'].strip()
        if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
            continue
        full_url = urljoin(target_url, href)
        unique_urls.add(full_url)

    print(f"Found {len(unique_urls)} unique links to verify.\n")

    for url in sorted(unique_urls):
        is_internal = urlparse(url).netloc == target_domain
        link_type = "Internal" if is_internal else "External"

        try:
            res = requests.head(url, allow_redirects=False, timeout=10)
            if res.status_code == 405:
                res = requests.get(url, allow_redirects=False, timeout=10)

            if res.status_code == 200:
                # print(f"[OK] {link_type}: {url}")
                pass
            elif res.status_code in (301, 302, 303, 307, 308):
                redirect_target = res.headers.get('Location', 'Unknown')
                print(f"[REDIRECT ERROR] {link_type} link redirected (Status {res.status_code}):\n  Source: {url}\n  Target: {redirect_target}\n")
            else:
                print(f"[BROKEN] {link_type} link failed with Status {res.status_code}:\n  URL: {url}\n")

        except requests.exceptions.Timeout:
            print(f"[TIMEOUT ERROR] {link_type} link timed out:\n  URL: {url}\n")
        except requests.exceptions.RequestException as e:
            print(f"[CONNECTION ERROR] {link_type} link failed to resolve:\n  URL: {url}\n  Error: {e}\n")

if __name__ == "__main__":
    # Check if the user actually provided a URL argument
    if len(sys.argv) < 2:
        print("Error: Please provide a target URL.")
        print("Usage: python link_checker.py <URL>")
        sys.exit(1)
    
    # Grab the first argument after the script name
    user_url = sys.argv[1]
    check_links(user_url)