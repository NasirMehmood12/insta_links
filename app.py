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






# from flask import Flask, render_template
# import psycopg2
# import os

# app = Flask(__name__)

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://save_links_user:9WO8M1bIXq1nd4SSzW3uyTeaFzjmBC8M@dpg-curg0123esus73dnsv7g-a.oregon-postgres.render.com/save_links")

# def get_links():
#     """Fetch links from the PostgreSQL database."""
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()
#         cursor.execute("SELECT page_name, link FROM instagram_links")  # Removed "scraped_at"
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         return data  # Returning list of tuples (page_name, link)

#     except Exception as e:
#         return []

# @app.route("/")
# def index():
#     """Render links in an HTML table."""
#     links = get_links()
#     return render_template("index.html", links=links)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)




from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://save_links_user:9WO8M1bIXq1nd4SSzW3uyTeaFzjmBC8M@dpg-curg0123esus73dnsv7g-a.oregon-postgres.render.com/save_links")

# Hardcoded username and password
USERNAME = "IMM"
PASSWORD = "imm@geotv"

# def get_links():
#     """Fetch links from the PostgreSQL database."""
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()
#         cursor.execute("SELECT page_name, link FROM instagram_links")
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return data  # Returning list of tuples (page_name, link)
#     except Exception as e:
#         return []


# def get_links():
#     """Fetch links from both Instagram and Facebook tables."""
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT page_name, link FROM instagram_links
#             UNION ALL
#             SELECT page_name, link FROM facebook_links
#         """)
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return data  # Returning list of tuples (page_name, link)
#     except Exception as e:
#         print(f"Error fetching links: {e}")
#         return []



# def get_links():
#     """Fetch links separately from Instagram and Facebook tables."""
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()

#         # Fetch Instagram links
#         cursor.execute("SELECT page_name, link FROM instagram_links")
#         instagram_links = cursor.fetchall()

#         # Fetch Facebook links
#         cursor.execute("SELECT page_name, link FROM facebook_links")
#         facebook_links = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         return instagram_links, facebook_links  # Return as two separate lists

#     except Exception as e:
#         print(f"Error fetching links: {e}")
#         return [], []  # Return empty lists in case of an error



# @app.route("/", methods=["GET", "POST"])
# def login():
#     """Login Page"""
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         if username == USERNAME and password == PASSWORD:
#             session["user"] = username  # Store user session
#             return redirect(url_for("index"))  # Redirect to links page
#         else:
#             return render_template("login.html", error="Invalid credentials")
    
#     return render_template("login.html")

# @app.route("/links")
# def index():
#     """Show links only if logged in"""
#     if "user" not in session:
#         return redirect(url_for("login"))  # Redirect to login if not logged in
    
#     # links = get_links()
#     # return render_template("index.html", links=links)
#     instagram_links, facebook_links = get_links()
#     return render_template("index.html", instagram_links=instagram_links, facebook_links=facebook_links)

# @app.route("/logout")
# def logout():
#     """Logout and clear session"""
#     session.pop("user", None)
#     return redirect(url_for("login"))

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)




def get_instagram_links():
    """Fetch Instagram links from the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        # cursor.execute("SELECT page_name, link FROM instagram_links")
        # cursor.execute('SELECT page_name, link, TO_CHAR("timestamp", \'YYYY-MM-DD HH24:MI:SS\') FROM instagram_links')
        data = [(page, link, str(timestamp)) for page, link, timestamp in cursor.fetchall()]

        # data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching Instagram links: {e}")
        return []

def get_facebook_links():
    """Fetch Facebook links from the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT page_name, link FROM facebook_links")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching Facebook links: {e}")
        return []

@app.route("/links")
def index():
    """Show links only if logged in"""
    if "user" not in session:
        return redirect(url_for("login"))  

    instagram_links = get_instagram_links()
    facebook_links = get_facebook_links()

    instagram_pages = list(set([link[0] for link in instagram_links]))  
    facebook_pages = list(set([link[0] for link in facebook_links]))

    return render_template("index.html", 
                           instagram_links=instagram_links, 
                           facebook_links=facebook_links, 
                           instagram_pages=instagram_pages, 
                           facebook_pages=facebook_pages)




@app.route("/", methods=["GET", "POST"])
def login():
    """Login Page"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username  # Store user session
            return redirect(url_for("index"))  # Redirect to links page
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")



@app.route("/logout")
def logout():
    """Logout and clear session"""
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000,)

