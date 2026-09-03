"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  KYNEXAUTH PYTHON WEB PORTAL APPLICATION                   ║
║                     Flask Web Authentication Server                        ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from kynexauth import KynexAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# -------------------------------------------------------------
# CONFIGURE YOUR APPLICATION CREDENTIALS
# -------------------------------------------------------------
kynex_app = KynexAuth(
    name="your app",
    owner_id="YOUR VERRSION",
    version="YOUR VERSION",
    url="https://kynexauth.com/api/v1/client",
)


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))

    # Initialize connection
    if not kynex_app.init():
        flash(f"Initialization Failed: {kynex_app.response.message}", "error")

    if request.method == "POST":
        action = request.form.get("action", "login")

        if action == "login":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()

            if not username or not password:
                flash("Username and password are required.", "error")
            elif kynex_app.login(username, password):
                session["user"] = {
                    "username": kynex_app.user_data.username,
                    "ip": kynex_app.user_data.ip or "127.0.0.1",
                    "hwid": kynex_app.user_data.hwid,
                    "createdate": kynex_app.user_data.createdate,
                    "lastlogin": kynex_app.user_data.lastlogin,
                    "subscriptions": [
                        {"name": s.name, "expiry": s.expiry}
                        for s in kynex_app.user_data.subscriptions
                    ],
                }
                return redirect(url_for("dashboard"))
            else:
                flash(kynex_app.response.message, "error")

        elif action == "register":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            key = request.form.get("license", "").strip()
            email = request.form.get("email", "").strip()

            if not username or not password or not key:
                flash("Username, password, and license key are required.", "error")
            elif kynex_app.register(username, password, key, email):
                flash("Registration successful! You can now log in.", "success")
            else:
                flash(kynex_app.response.message, "error")

        elif action == "license":
            key = request.form.get("license", "").strip()
            if not key:
                flash("License key is required.", "error")
            elif kynex_app.license(key):
                session["user"] = {
                    "username": kynex_app.user_data.username,
                    "ip": kynex_app.user_data.ip or "127.0.0.1",
                    "hwid": kynex_app.user_data.hwid,
                    "createdate": kynex_app.user_data.createdate,
                    "lastlogin": kynex_app.user_data.lastlogin,
                    "subscriptions": [
                        {"name": s.name, "expiry": s.expiry}
                        for s in kynex_app.user_data.subscriptions
                    ],
                }
                return redirect(url_for("dashboard"))
            else:
                flash(kynex_app.response.message, "error")

        elif action == "upgrade":
            username = request.form.get("username", "").strip()
            key = request.form.get("license", "").strip()

            if not username or not key:
                flash("Username and renewal license key are required.", "error")
            elif kynex_app.upgrade(username, key):
                flash("Subscription extended successfully! Please log in.", "success")
            else:
                flash(kynex_app.response.message, "error")

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("\n  ======================================================")
    print("  🐍 KynexAuth Python Web Server Running!")
    print("  🌐 URL: http://localhost:5000")
    print("  ======================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
