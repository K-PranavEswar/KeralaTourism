from flask import Flask, render_template, request
import os
import csv

app = Flask(__name__)

CSV_FILE = "kerala-tourism.csv"

# Create CSV file only if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Message"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/destinations")
def destinations():
    return render_template("destinations.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "message": request.form.get("message")
    }

    # Append data to CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data["name"], data["email"], data["message"]])

    return render_template("contact.html", success=True, data=data)

if __name__ == "__main__":
    app.run(debug=True)