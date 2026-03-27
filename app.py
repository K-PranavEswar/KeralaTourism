from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

# CSV file path (Render safe)
CSV_FILE = os.path.join(os.getcwd(), "kerala-tourism.csv")

# Create CSV file at startup (if not exists)
if not os.path.isfile(CSV_FILE):
    try:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Email", "Message"])
        print("CSV file created successfully")
    except Exception as e:
        print("Error creating CSV:", e)

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
    return render_template("contact.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    try:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])
        print("Data saved:", name)
    except Exception as e:
        print("Error saving data:", e)

    return redirect(url_for('contact', success=1))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)