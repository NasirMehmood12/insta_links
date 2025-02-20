from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection (Update for Render deployment)
DATABASE_URL = os.getenv("DATABASE_URL", "dbname=save_links user=postgres password=password host=localhost port=5432")

def get_links():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT page_name, link, scraped_at FROM instagram_links ORDER BY scraped_at DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

@app.route("/")
def index():
    links = get_links()
    return render_template("index.html", links=links)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
