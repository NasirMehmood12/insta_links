# from flask import Flask, jsonify
# import psycopg2
# import os

# app = Flask(__name__)

# # -------------------------------
# # Configure PostgreSQL connection (Render Database)
# # -------------------------------
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://save_links_user:9WO8M1bIXq1nd4SSzW3uyTeaFzjmBC8M@dpg-curg0123esus73dnsv7g-a.oregon-postgres.render.com/save_links")

# def get_links():
#     """Fetch links from the PostgreSQL database."""
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()
#         cursor.execute("SELECT page_name, link, scraped_at FROM instagram_links ORDER BY scraped_at DESC")
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         # Convert data to a list of dictionaries
#         links = [{"page_name": row[0], "link": row[1], "scraped_at": row[2]} for row in data]
#         return links

#     except Exception as e:
#         return {"error": str(e)}

# @app.route("/")
# def index():
#     """API endpoint to return the scraped links."""
#     links = get_links()
#     return jsonify(links)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)






from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://save_links_user:9WO8M1bIXq1nd4SSzW3uyTeaFzjmBC8M@dpg-curg0123esus73dnsv7g-a.oregon-postgres.render.com/save_links")

def get_links():
    """Fetch links from the PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT page_name, link FROM instagram_links")  # Removed "scraped_at"
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data  # Returning list of tuples (page_name, link)

    except Exception as e:
        return []

@app.route("/")
def index():
    """Render links in an HTML table."""
    links = get_links()
    return render_template("index.html", links=links)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
