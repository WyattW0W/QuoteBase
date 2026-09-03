from flask import Flask, request, jsonify, redirect, url_for, render_template
import json

with open("quotes.json", "r") as f:
    quotes = json.load(f)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html"), 200

@app.route("/quotes", methods=["GET"])
def get_quotes():
    return render_template("quotes.html", quotes=quotes), 200

@app.route("/add-quote-template", methods=["GET"])
def add_quote_template():
    return render_template("add_quote.html"), 200

@app.route("/add-quote", methods=["POST"])
def add_quote():
    new_quote = request.get_json().get("text")
    new_author = request.get_json().get("author")
    if new_quote and new_author:
        quotes.append({"text": new_quote, "author": new_author})
        with open("quotes.json", "w") as f:
            json.dump(quotes, f)
        return jsonify({"message": "Quote added successfully!"}), 201
    else:
        return "Quote cannot be empty", 400

@app.route("/cat-and-mouse", methods=["GET"])
def cat_and_mouse():
    return render_template("cat_and_mouse.html"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
