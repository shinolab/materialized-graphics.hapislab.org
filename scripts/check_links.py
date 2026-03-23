import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def check_links(base_url):
    visited = set()
    to_visit = [base_url]
    # Map of target_url -> [source_urls]
    broken_links = {}

    print(f"Starting link check on {base_url}...")

    # Track where each link came from
    source_map = {base_url: "Root"}

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)
        print(f"Checking: {current_url}")

        try:
            # For internal links, we use GET to crawl. For external, HEAD might be enough but let's stay simple.
            response = requests.get(current_url, timeout=10, allow_redirects=True)

            if response.status_code == 404:
                source = source_map.get(current_url, "Unknown")
                if current_url not in broken_links:
                    broken_links[current_url] = []
                broken_links[current_url].append(source)
                continue

            if response.status_code != 200:
                print(
                    f"  Warning: {current_url} returned status code {response.status_code}"
                )
                continue

            # Only crawl HTML content from internal links
            if not current_url.startswith(
                base_url
            ) or "text/html" not in response.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all("a", href=True):
                link = a["href"]

                # Skip mailto, tel, etc.
                if link.startswith(("mailto:", "tel:", "javascript:", "#")):
                    continue

                full_url = urljoin(current_url, link)

                # Normalize URL (remove fragments)
                parsed_url = urlparse(full_url)
                normalized_url = parsed_url._replace(fragment="").geturl()

                if normalized_url not in visited and normalized_url not in to_visit:
                    if normalized_url.startswith(base_url):
                        to_visit.append(normalized_url)
                        source_map[normalized_url] = current_url
                    else:
                        # For external links, we can optionally check them here
                        # For now, let's just focus on internal consistency
                        pass

        except Exception as e:
            if current_url not in broken_links:
                broken_links[current_url] = []
            broken_links[current_url].append(
                f"Error: {str(e)} (from {source_map.get(current_url, 'Unknown')})"
            )
            print(f"  Error checking {current_url}: {e}")

    return broken_links, visited


if __name__ == "__main__":
    # Ensure URL ends with / if it's the root
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4321/"
    if not target_url.endswith("/") and urlparse(target_url).path == "":
        target_url += "/"

    start_time = time.time()
    broken, visited = check_links(target_url)
    duration = time.time() - start_time

    print(f"\nScan completed in {duration:.2f} seconds.")
    print(f"Total pages visited: {len(visited)}")

    if broken:
        print(f"\n{len(broken)} broken links found:")
        for url, sources in broken.items():
            print(f"\nBroken URL: {url}")
            print(f"  Found on pages:")
            for s in sources:
                print(f"    - {s}")
        sys.exit(1)
    else:
        print("\nNo broken links found!")
        sys.exit(0)
