from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, Response
import joblib
import numpy as np
from datetime import datetime, timedelta
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import csv
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- JWT SETTINGS ----------------
JWT_SECRET = "your_jwt_secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_HOURS = 1


def create_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXP_HOURS)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("username")
    except (ExpiredSignatureError, InvalidTokenError):
        return None


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.cookies.get("jwt")

        if not token:
            return redirect(url_for("login"))

        username = decode_jwt(token)

        if not username:
            return redirect(url_for("login"))

        return f(username, *args, **kwargs)

    return decorated


# ---------------- LOAD ML MODEL ----------------
try:
    model = joblib.load("ml/model.pkl")
except:
    model = None
    print("⚠️ ML model not loaded")


# ---------------- DATABASE ----------------
DB_NAME = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        timestamp TEXT,
        ip_address TEXT,
        device INTEGER,
        browser INTEGER,
        country INTEGER,
        failed_attempts INTEGER,
        prediction INTEGER
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HELPERS ----------------
failed_attempts_store = {}


def get_device_browser(user_agent):

    ua = user_agent.lower()

    device = 1 if "mobile" in ua else 0

    if "chrome" in ua:
        browser = 1
    elif "firefox" in ua:
        browser = 2
    else:
        browser = 3

    return device, browser


def get_country_from_ip(ip):

    if ip.startswith("127.") or ip.startswith("192."):
        return 0
    return 2


# ---------------- LOG FUNCTION ----------------
def log_attempt(username, ip, device, browser, country,
                failed_attempts, prediction):

    conn = get_db_connection()

    conn.execute("""
    INSERT INTO login_logs
    (username,timestamp,ip_address,device,browser,country,failed_attempts,prediction)
    VALUES (?,?,?,?,?,?,?,?)
    """, (
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ip,
        device,
        browser,
        country,
        failed_attempts,
        prediction
    ))

    conn.commit()
    conn.close()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")

        if username not in failed_attempts_store:
            failed_attempts_store[username] = 0

        ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        device, browser = get_device_browser(
            request.headers.get("User-Agent", "")
        )

        country = get_country_from_ip(ip)

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        # USER NOT FOUND
        if not user:

            failed_attempts_store[username] += 1
            prediction = 1 if failed_attempts_store[username] >= 5 else 0

            log_attempt(username, ip, device, browser,
                        country, failed_attempts_store[username], prediction)

            return render_template("index.html", message="❌ User not found")

        # WRONG PASSWORD
        if not check_password_hash(user["password_hash"], password):

            failed_attempts_store[username] += 1
            prediction = 1 if failed_attempts_store[username] >= 5 else 0

            log_attempt(username, ip, device, browser,
                        country, failed_attempts_store[username], prediction)

            return render_template("index.html", message="❌ Invalid credentials")

        # SUCCESS LOGIN
        failed_attempts_store[username] = 0
        prediction = 0

        if model:

            hour = datetime.now().hour
            features = np.array([[hour, 0, device, browser, country]])

            prediction = int(model.predict(features)[0])

        log_attempt(username, ip, device, browser, country, 0, prediction)

        if prediction == 1:
            return render_template("index.html", message="⚠️ Suspicious login")

        token = create_jwt(username)

        # redirect admin / user
        if username == "admin":
            resp = make_response(redirect(url_for("admin")))
        else:
            resp = make_response(redirect(url_for("home")))

        resp.set_cookie("jwt", token, httponly=True, samesite="Strict")

        return resp

    return render_template("index.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():

    username = request.form.get("username").strip()
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return render_template("index.html", message="❌ Passwords do not match")

    password_hash = generate_password_hash(password)

    conn = get_db_connection()

    try:

        conn.execute(
            "INSERT INTO users(username,password_hash) VALUES(?,?)",
            (username, password_hash)
        )

        conn.commit()
        conn.close()

        return render_template("index.html", message="✅ Registration successful!")

    except sqlite3.IntegrityError:

        conn.close()
        return render_template("index.html", message="⚠️ Username already exists")


# ---------------- HOME ----------------
@app.route("/home")
@jwt_required
def home(username):
    return render_template("home.html", username=username)

@app.route("/attacks")
@jwt_required
def attacks(username):
    return render_template("attacks.html")


@app.route("/measures")
@jwt_required
def measures(username):
    return render_template("measures.html")


@app.route("/impact")
@jwt_required
def impact(username):
    return render_template("impact.html")


@app.route("/tips")
@jwt_required
def tips(username):
    return render_template("tips.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
@jwt_required
def admin(username):

    if username != "admin":
        return "Unauthorized", 403

    conn = get_db_connection()

    logs = conn.execute(
        "SELECT * FROM login_logs ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("admin.html", logs=[dict(row) for row in logs])


# ---------------- CSV EXPORT ----------------
@app.route("/export/csv")
@jwt_required
def export_csv(username):

    if username != "admin":
        return "Unauthorized", 403

    conn = get_db_connection()

    logs = conn.execute(
        "SELECT * FROM login_logs ORDER BY id DESC"
    ).fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Username", "Timestamp", "IP",
        "Device", "Browser", "Country",
        "Fails", "Status"
    ])

    for log in logs:

        writer.writerow([
            log["id"],
            log["username"],
            log["timestamp"],
            log["ip_address"],
            log["device"],
            log["browser"],
            log["country"],
            log["failed_attempts"],
            "Suspicious" if log["prediction"] == 1 else "Normal"
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=login_logs.csv"}
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("jwt")

    return resp


if __name__ == "__main__":
    app.run(debug=True)