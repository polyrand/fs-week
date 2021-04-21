try:
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_hash(plain_password, hashed_password):
        """
        This functions returns True if the password matches the hash,
        otherwise it returns False
        """

        return pwd_context.verify(plain_password, hashed_password)

    def get_hash(password):
        return pwd_context.hash(password)


except:

    # adapted from https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    import hashlib

    salt = "caf38121a3841ff2083cf5bf7a35ea58a9fe43351a2ff0cabfd4ef6696bdc39f"

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100000
        ).hex()

    def verify_hash(plain_password, hashed_password):

        password_to_check = plain_password  # The password provided by the user to check

        # Use the exact same setup you used to generate the key, but this time put in the password to check
        new_key = hashlib.pbkdf2_hmac(
            "sha256",
            password_to_check.encode("utf-8"),  # Convert the password to bytes
            bytes.fromhex(salt),
            100000,
        ).hex()

        if new_key == hashed_password:
            return True
        else:
            return False


from pathlib import Path
from uuid import uuid4
import datetime as dt
import os
import requests
import sqlite3


from flask import Flask, jsonify, render_template, request

# def print(*args, **kwargs):
#     return


template_dir = Path("../templates")
app = Flask(__name__, template_folder=str(template_dir))


class DB:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

        # self.conn.execute("")

        with self.conn as c:
            c.executescript(
                """
CREATE TABLE IF NOT EXISTS logs (time TEXT, key TEXT, value TEXT);
CREATE TABLE IF NOT EXISTS users (user_id TEXT, email TEXT, password TEXT);
""".strip()
            )

    def create_user(self, email, password):

        hashed_password = get_hash(password)
        new_user_id = str(uuid4())
        with self.conn as c:
            c.execute(
                "insert into users values (?, ?, ?)",
                (new_user_id, email, hashed_password),
            )

        return new_user_id

    def validate_password(self, email, password):
        """This function receives an email and password and checks
        if that's the password associated with that email.

        If the they don't match it returns None, if they match
        it will return the user_id associated with that user.
        """

        user = self.conn.execute(
            "select * from users where email = ?", (email,)
        ).fetchone()

        print(user)

        if not user:
            return None
        else:
            user_id = user[0]
            email = user[1]
            hashed_password = user[2]

            print(password, hashed_password)

            if not verify_hash(password, hashed_password):
                return None
            else:
                return user_id

    def log_message(self, key, value):

        now = dt.datetime.utcnow().isoformat()

        with self.conn as c:
            c.execute("INSERT INTO logs VALUES (?, ?, ?)", (now, key, value))
        return


# we still need to implement user creation (using another HTML form)
db = DB(dbname="ml_app.db")


@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")


@app.route("/create_user", methods=["GET", "POST"])
def user_create():

    if request.method == "GET":
        return render_template("create_user.html")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["new_user_password"]

        db.create_user(email=email, password=password)

        return "ok"


@app.route("/file_upload", methods=["POST"])
def post_image():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["user_key"]

        print(email, password)

        if not db.validate_password(email=email, password=password):
            return "not allowed"

        file = request.files["file_1"]

        img_bytes = file.read()

        r = requests.post("http://127.0.0.1:5005/predict", files={"file": img_bytes})

        r.raise_for_status()

        # return r.json()

        result_class = r.json()

        return render_template("response.html", response=result_class)
