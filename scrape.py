from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from requests.exceptions import ConnectionError

fname = "scraped-tasks-for-writeups.csv"
verbose = 1

def process_url(i):
    url = f"https://ctftime.org/tasks/{i}"
    retries = 3
    errordelay = 2  # Delay in seconds between retries
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    while retries > 0:
        try:
            if verbose: print(f"[.] Trying page {url}")
            time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
            response = requests.get(url, headers=headers)
            if verbose: print(f"[.] Trying raise_for_status()")
            response.raise_for_status()
            html_content = response.text
            print(f"[.] Parsing with BS4")
            soup = BeautifulSoup(html_content, 'html.parser')
            if verbose: print(f"[.] Finding task links..")
            task_links = soup.find_all('a', href=lambda href: href and href.startswith('/task'))
            if verbose: print(f"[.] Creating task variables..")
            task_urls = [link['href'] for link in task_links]
            print(f"[.] Writing to {fname}")
            with open(fname, "a") as f:
                f.write(f"task,url\n")
                for url in task_urls:
                    print(url)
                    f.write(f"{i},{url}\n")
                return
        except (ConnectionError, requests.exceptions.RequestException) as e:
            retries -= 1
            if retries > 0:
                print(f"[!] Error: couldn't get page {url}, error {e} - Retrying in {errordelay} seconds...")
                time.sleep(errordelay)
            else:
                print(f"[!] Error: couldn't get page {url}, skipping. Error: {e}")
                return


delay=1  # Main loop delay

with ThreadPoolExecutor() as executor:
    for i in range(120, 27800):
        futures = executor.submit(process_url, i)
        time.sleep(delay)
    for future in as_completed(futures):
        future.result()
