from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory user storage
users = {}


@app.route("/")
def index():
    if "email" in session:
        user = users.get(session["email"])
        if user:
            return render_template("index.html", user=user)
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    if email in users:
        # flash("Email already registered.", "danger")
        return redirect(url_for("index"))

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    users[email] = {
        "email": email,
        "name": name,
        "password": hashed_password,
        "role": role,
    }

    # flash("Registration successful! Please login.", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = users.get(email)

    if not user or not check_password_hash(user["password"], password):
        # flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for("index"))

    # flash(f'Welcome, {user["name"]}!', "success")
    session["email"] = user["email"]
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("email", None)
    # flash("You have been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
