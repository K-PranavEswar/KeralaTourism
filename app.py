from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

CSV_FILE = os.path.join(os.getcwd(), "kerala-tourism.csv")

# Create CSV file if not exists
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
    success = request.args.get("success")
    return render_template("contact.html", success=success)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    print("Received:", name, email, message)

    if not name or not email or not message:
        print("Invalid form data")
        return redirect(url_for('contact', success=0))

    try:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])

        print("Data saved successfully")

    except Exception as e:
        print("Error saving data:", e)
        return redirect(url_for('contact', success=0))

    return redirect(url_for('contact', success=1))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)