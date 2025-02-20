# from flask import Flask, render_template, jsonify
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time
# import pickle

# app = Flask(__name__)

# # List of Instagram pages
# pages = [
#     {"name": "Dailymail", "url": "https://www.instagram.com/dailymail"},
#     {"name": "BBC News", "url": "https://www.instagram.com/bbcnews"}
# ]

# def get_instagram_links(page_url):
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=375,812")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36")
    
#     driver = webdriver.Chrome(options=options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)
    
#     try:
#         cookies = pickle.load(open("instagram_cookies.pkl", "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#     except Exception as e:
#         return {"error": f"Error loading cookies: {e}"}
    
#     driver.get(page_url)
#     time.sleep(5)
    
#     links = driver.find_elements(By.TAG_NAME, "a")
#     extracted_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and ("/p/" in link.get_attribute("href") or "/reel/" in link.get_attribute("href"))]
    
#     driver.quit()
#     return extracted_links

# @app.route('/')
# def index():
#     return render_template("index.html", pages=pages)

# @app.route('/get-links/<page_name>')
# def get_links(page_name):
#     page = next((p for p in pages if p["name"] == page_name), None)
#     if not page:
#         return jsonify({"error": "Page not found"}), 404
    
#     links = get_instagram_links(page["url"])
#     return jsonify({"page": page_name, "links": links})

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import json
import time

app = Flask(__name__)

# List of Instagram pages
pages = [
    {"name": "Dailymail", "url": "https://www.instagram.com/dailymail"},
    {"name": "BBC News", "url": "https://www.instagram.com/bbcnews"}
]

def get_instagram_links(page_url):
    # Chrome options for Render deployment
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Prevent session conflicts
    options.add_argument("--no-sandbox")  # Required for cloud environments
    options.add_argument("--disable-dev-shm-usage")  # Helps on low-memory systems

    # Start Selenium WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    # Load cookies from Environment Variable
    try:
        cookies_json = os.getenv("INSTAGRAM_COOKIES")  # Fetch from Render env variables
        if cookies_json:
            cookies = json.loads(cookies_json)
            for cookie in cookies:
                driver.add_cookie(cookie)
        else:
            return {"error": "No cookies found in environment variables"}
    except Exception as e:
        return {"error": f"Error loading cookies: {e}"}

    # Go to the target Instagram page
    driver.get(page_url)
    time.sleep(5)

    # Extract links from posts and reels
    links = driver.find_elements(By.TAG_NAME, "a")
    extracted_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and ("/p/" in link.get_attribute("href") or "/reel/" in link.get_attribute("href"))]

    driver.quit()
    return extracted_links

@app.route('/')
def index():
    return render_template("index.html", pages=pages)

@app.route('/get-links/<page_name>')
def get_links(page_name):
    page = next((p for p in pages if p["name"] == page_name), None)
    if not page:
        return jsonify({"error": "Page not found"}), 404
    
    links = get_instagram_links(page["url"])
    return jsonify({"page": page_name, "links": links})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)  # Render uses port 10000
