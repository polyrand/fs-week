import logging
import requests

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/submit", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def post_image():

    if request.method == "POST":
        file = request.files["file"]
        img_bytes = file.read()

        r = requests.post("http://127.0.0.1:5000/predict", files={"file": img_bytes})

        r.raise_for_status()

        return render_template("response.html")
