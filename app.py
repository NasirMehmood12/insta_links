# from flask import Flask, render_template, jsonify
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# app = Flask(__name__)

# # Selenium WebDriver (Use headless mode for deployment)
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# # List of Instagram pages
# pages = [
#     {"name": "Kim Kardashian", "url": "https://www.instagram.com/kimkardashian/"},
#     {"name": "Kylie Jenner", "url": "https://www.instagram.com/kyliejenner/"},
#     {"name": "Rihanna", "url": "https://www.instagram.com/badgalriri/"},
#     {"name": "Kanye West", "url": "https://www.instagram.com/ye/"},
# ]

# # Scraping Function
# def scrape_instagram_links(page_url):
#     extracted_links = []
#     driver.get(page_url)
#     time.sleep(10)  # Wait for page to load

#     links = driver.find_elements(By.TAG_NAME, "a")
#     for link in links:
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             extracted_links.append(url)

#     return extracted_links

# # Route for Frontend
# @app.route('/')
# def index():
#     return render_template("index.html", pages=pages)

# # API Route for Fetching Links
# @app.route('/get-links/<page_name>')
# def get_links(page_name):
#     page = next((p for p in pages if p["name"] == page_name), None)
#     if not page:
#         return jsonify({"error": "Page not found"}), 404

#     links = scrape_instagram_links(page["url"])
#     return jsonify({"page": page_name, "links": links})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__, template_folder="templates")

# Configure headless Chrome for Render
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# List of Instagram pages
pages = [
    {"name": "Kim Kardashian", "url": "https://www.instagram.com/kimkardashian/"},
    {"name": "Kylie Jenner", "url": "https://www.instagram.com/kyliejenner/"},
    {"name": "Rihanna", "url": "https://www.instagram.com/badgalriri/"},
    {"name": "Kanye West", "url": "https://www.instagram.com/ye/"},
]

# Homepage Route (Fixes 404 Error)
@app.route('/')
def home():
    return render_template("index.html", pages=pages)

# Function to scrape Instagram links
def scrape_instagram_links(page_name):
    extracted_links = []
    for page in pages:
        if page["name"] == page_name:
            driver.get(page["url"])
            time.sleep(10)

            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                url = link.get_attribute("href")
                if url and ("/p/" in url or "/reel/" in url):
                    extracted_links.append(url)
            break
    return extracted_links

# API to get links for a specific page
@app.route('/get-links/<string:page_name>', methods=['GET'])
def get_instagram_links(page_name):
    links = scrape_instagram_links(page_name)
    return jsonify({"page": page_name, "links": links})

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, jsonify
# from playwright.sync_api import sync_playwright

# app = Flask(__name__)

# def scrape_instagram_links(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
#         page = browser.new_page()
#         page.goto(url)
#         page.wait_for_timeout(15000)  # Wait for the page to load completely
#         anchors = page.query_selector_all("a")
#         post_links = [a.get_attribute("href") for a in anchors if a.get_attribute("href") and "/p/" in a.get_attribute("href")]
#         browser.close()
#     return post_links

# # Sample pages list
# pages = [
#     {"name": "Kylie Jenner", "url": "https://www.instagram.com/kyliejenner/"},
#     # Add more pages as needed
# ]

# @app.route("/get-links/<string:page_name>", methods=["GET"])
# def get_instagram_links(page_name):
#     # Find the page from the list
#     page_data = next((page for page in pages if page["name"] == page_name), None)
#     if not page_data:
#         return jsonify({"error": "Page not found"}), 404
#     links = scrape_instagram_links(page_data["url"])
#     return jsonify({"page": page_name, "links": links})

# if __name__ == "__main__":
#     app.run(debug=True)
