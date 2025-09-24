import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

BOT_DIR = os.path.dirname(__file__)
COOKIES_JSON = os.path.join(BOT_DIR, "cookies.json")
COOKIES_TXT = os.path.join(BOT_DIR, "cookies.txt")

def save_cookies_netscape(cookies, out_file):
    """Convert Selenium cookies to Netscape format for yt-dlp."""
    lines = ["# Netscape HTTP Cookie File", f"# Converted: {datetime.utcnow().isoformat()}"]
    for c in cookies:
        domain = c.get("domain", "")
        flag = "TRUE" if domain.startswith(".") else "FALSE"
        path = c.get("path", "/")
        secure = "TRUE" if c.get("secure") else "FALSE"
        expires = str(int(c.get("expiry") or 0))
        name = c.get("name")
        value = c.get("value")
        lines.append("\t".join([domain, flag, path, secure, expires, name, value]))
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved cookies to {out_file}")

def get_cookies_from_site(url):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # remove headless for manual login
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    print(f"Please log in manually in the browser that opened: {url}")
    input("After login, press Enter here...")

    cookies = driver.get_cookies()
    driver.quit()

    # Save JSON
    with open(COOKIES_JSON, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    print(f"Saved cookies JSON to {COOKIES_JSON}")

    # Save Netscape cookies.txt
    save_cookies_netscape(cookies, COOKIES_TXT)

if __name__ == "__main__":
    site_url = input("Enter site URL to login: ").strip()
    get_cookies_from_site(site_url)
