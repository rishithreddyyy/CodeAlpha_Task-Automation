"""
Task 3: Scrape the title of a fixed webpage and save it
Key Concepts: requests, re (Regular Expressions), file handling, os

This script uses the 'requests' library to fetch the HTML content of a webpage,
parses the <title> tag using regular expressions ('re'), sanitizes the text,
and saves the extracted title along with metadata into a designated text file.
"""

import os
import re
import html
import sys
import argparse
from datetime import datetime
import requests


# Default webpage URL (reliable and standard)
DEFAULT_URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
DEFAULT_OUTPUT_FILE = "scraped_title.txt"

# Standard User-Agent header to avoid 403 Forbidden from strict servers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36 TaskAutomationBot/1.0"
    )
}


def extract_title_with_regex(html_content: str) -> str:
    """
    Extracts the content of the <title> tag from HTML using regular expressions.
    Cleans up HTML entities and whitespace.
    """
    # Regex pattern to match <title>...</title> case-insensitively, across newlines
    match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)

    if match:
        raw_title = match.group(1)
        # Unescape HTML entities (e.g., &amp; -> &, &quot; -> ", &#39; -> ')
        clean_title = html.unescape(raw_title)
        # Collapse multiple whitespaces and newlines into a single clean line
        clean_title = " ".join(clean_title.split()).strip()
        return clean_title
    return "No <title> tag found on page"


def scrape_and_save_title(url: str, output_path: str, timeout: int = 10) -> dict:
    """
    Fetches the given URL, extracts the webpage title, and saves it to a file.

    Returns:
        dict: Result containing status, title, url, and metadata.
    """
    print("=" * 60)
    print("  WEBPAGE TITLE SCRAPER")
    print("=" * 60)
    print(f"Target URL : {url}")
    print(f"Output File: {os.path.abspath(output_path)}")
    print("-" * 60)

    result = {
        "success": False,
        "url": url,
        "title": None,
        "status_code": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        print(f"[*] Sending HTTP GET request to '{url}'...")
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        result["status_code"] = response.status_code

        print(f"[*] Response received with HTTP Status: {response.status_code}")

        # Check for HTTP errors (4xx, 5xx)
        response.raise_for_status()

        # Extract title using regular expression
        page_title = extract_title_with_regex(response.text)
        result["title"] = page_title
        result["success"] = True

        print(f"\n[+] Extracted Webpage Title:\n    \"{page_title}\"")

        # Ensure destination directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        # Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("WEBPAGE TITLE SCRAPE RESULT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Scraped At   : {result['timestamp']}\n")
            f.write(f"Target URL   : {url}\n")
            f.write(f"HTTP Status  : {response.status_code}\n")
            f.write(f"Content-Type : {response.headers.get('Content-Type', 'N/A')}\n")
            f.write("-" * 60 + "\n")
            f.write(f"PAGE TITLE:\n{page_title}\n")
            f.write("=" * 60 + "\n")

        print(f"\n[SAVED] Title successfully written to '{os.path.abspath(output_path)}'")
        print("=" * 60)

    except requests.exceptions.Timeout:
        error_msg = f"Request timed out after {timeout} seconds."
        print(f"[ERROR] {error_msg}")
        result["error"] = error_msg
    except requests.exceptions.ConnectionError:
        error_msg = "Network connection failed or host not reachable."
        print(f"[ERROR] {error_msg}")
        result["error"] = error_msg
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error occurred: {e}"
        print(f"[ERROR] {error_msg}")
        result["error"] = error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        print(f"[ERROR] {error_msg}")
        result["error"] = error_msg

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape the title of a webpage and save to file.")
    parser.add_argument("--url", "-u", type=str, default=None, help=f"Webpage URL to scrape (default: {DEFAULT_URL})")
    parser.add_argument("--output", "-o", type=str, default=None, help=f"Output file path (default: {DEFAULT_OUTPUT_FILE})")
    args = parser.parse_args()

    if args.url and args.output:
        url = args.url
        output = args.output
    else:
        print("Task Automation - Option 3: Scrape Webpage Title")
        url = args.url or input(f"Enter webpage URL [default: '{DEFAULT_URL}']: ").strip() or DEFAULT_URL
        output = args.output or input(f"Enter output file path [default: '{DEFAULT_OUTPUT_FILE}']: ").strip() or DEFAULT_OUTPUT_FILE

    scrape_and_save_title(url, output)


if __name__ == "__main__":
    main()
