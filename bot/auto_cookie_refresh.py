import json
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BOT_DIR = os.path.dirname(__file__)
COOKIES_JSON = os.path.join(BOT_DIR, "cookies.json")
COOKIES_TXT = os.path.join(BOT_DIR, "cookies.txt")
COOKIE_EXPIRY_THRESHOLD = 3600 * 24 * 7  # 7 days

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
    print(f"[✓] Saved cookies to {out_file}")

def cookies_expired(json_file):
    if not os.path.exists(json_file):
        return True
    with open(json_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    now = time.time()
    for c in cookies:
        if c.get("expiry") and (c.get("expiry") - now) > COOKIE_EXPIRY_THRESHOLD:
            return False  # at least one cookie still valid
    return True

def refresh_cookies(url):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # remove headless to log in manually
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    print(f"[!] Please log in manually in the browser for {url}")
    input("After login, press Enter here...")

    cookies = driver.get_cookies()
    driver.quit()

    # Save JSON
    with open(COOKIES_JSON, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)

    # Save Netscape format for yt-dlp
    save_cookies_netscape(cookies, COOKIES_TXT)

def ensure_cookies(url):
    if cookies_expired(COOKIES_JSON):
        print("[!] Cookies missing or expired, refreshing...")
        refresh_cookies(url)
    else:
        print("[✓] Cookies are valid")

if __name__ == "__main__":
    site_url = input("Enter site URL to manage cookies: ").strip()
    ensure_cookies(site_url)
