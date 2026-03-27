from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_FILE = os.path.join(os.getcwd(), "database.db")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/destinations/")
def destinations():
    return render_template("destinations.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    success = request.args.get("success")
    return render_template("contact.html", success=success)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        return redirect(url_for('contact', success=0))

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()
        print("Data stored in DB")

    except Exception as e:
        print("DB Error:", e)
        return redirect(url_for('contact', success=0))

    return redirect(url_for('contact', success=1))


# 🔥 ADMIN PANEL
@app.route('/admin')
def admin():
    conn = get_db()
    data = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", data=data)


# 🔥 DELETE DATA
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)