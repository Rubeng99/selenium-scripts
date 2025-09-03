from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import time

# URL of the page
url = "https://www.nhc.noaa.gov/archive/recon/2025/REPRPD/"

# Folder to save the txt files
save_folder = "nhc_txt_files"
os.makedirs(save_folder, exist_ok=True)

# Start Selenium
driver = webdriver.Chrome()
driver.get(url)

# Give page a moment to load links
time.sleep(2)

# Find all links ending with .txt
txt_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.txt']")

print(f"Found {len(txt_links)} TXT files.")

# Download each file
for i, link in enumerate(txt_links, start=1):
    txt_url = link.get_attribute("href")
    if not txt_url:
        continue
    try:
        response = requests.get(txt_url, timeout=10)
        if response.status_code == 200:
            filename = os.path.join(save_folder, os.path.basename(txt_url))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[{i}] Saved {filename}")
        else:
            print(f"[{i}] Failed to download url {txt_url} (status {response.status_code})")
    except Exception as e:
        print(f"[{i}] Error downloading the url {txt_url}: {e}")
    finally:
        print("Done saving txt files to folder:", save_folder)

driver.quit()
