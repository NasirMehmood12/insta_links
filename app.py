from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

# Selenium WebDriver (Use headless mode for deployment)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# List of Instagram pages
pages = [
    {"name": "Kim Kardashian", "url": "https://www.instagram.com/kimkardashian/"},
    {"name": "Kylie Jenner", "url": "https://www.instagram.com/kyliejenner/"},
    {"name": "Rihanna", "url": "https://www.instagram.com/badgalriri/"},
    {"name": "Kanye West", "url": "https://www.instagram.com/ye/"},
]

# Scraping Function
def scrape_instagram_links(page_url):
    extracted_links = []
    driver.get(page_url)
    time.sleep(10)  # Wait for page to load

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        url = link.get_attribute("href")
        if url and ("/p/" in url or "/reel/" in url):
            extracted_links.append(url)

    return extracted_links

# Route for Frontend
@app.route('/')
def index():
    return render_template("index.html", pages=pages)

# API Route for Fetching Links
@app.route('/get-links/<page_name>')
def get_links(page_name):
    page = next((p for p in pages if p["name"] == page_name), None)
    if not page:
        return jsonify({"error": "Page not found"}), 404

    links = scrape_instagram_links(page["url"])
    return jsonify({"page": page_name, "links": links})

if __name__ == '__main__':
    app.run(debug=True)
