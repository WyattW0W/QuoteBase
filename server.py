from flask import Flask, request, jsonify, redirect, url_for, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html"), 200
