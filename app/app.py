import requests
import datetime as dt
from uuid import uuid4
import sqlite3
from pathlib import Path
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from flask import Flask, jsonify, render_template, request


template_dir = Path("templates")
app = Flask(__name__, template_folder=str(template_dir))


def verify_hash(plain_password, hashed_password):
    """
    This functions returns True if the password matches the hash,
    otherwise it returns False
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_hash(password):
    return pwd_context.hash(password)


class DB:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

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

        if not user:
            return None
        else:
            user_id = user[0]
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


@app.route("/file_upload", methods=["POST"])
def post_image():

    if request.method == "POST":
        password = request.form["user_key"]
        file = request.files["file_1"]
        print(file)
        img_bytes = file.read()

        r = requests.post("http://127.0.0.1:5001/predict", files={"file": img_bytes})

        r.raise_for_status()

        # return r.json()

        result_class = r.json()

        return render_template("response.html", response=result_class)
