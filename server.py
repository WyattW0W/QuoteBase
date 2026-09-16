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

@app.route("/quotes/add-quote", methods=["POST"])
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

@app.route("/delete-quote-template", methods=["GET"])
def delete_quote_template():
    return render_template("delete-quote.html", quotes=quotes), 200

@app.route("/quotes/delete-quote", methods=["POST"])
def delete_quote():
    global quotes

    quote_data = request.get_json(silent=True) or {}
    quote_to_delete = quote_data.get("text")
    author_to_delete = quote_data.get("author")

    if not quote_to_delete or not author_to_delete:
        return jsonify({"error": "Quote text and author cannot be empty"}), 400

    remaining_quotes = [
        quote for quote in quotes
        if quote.get("text") != quote_to_delete
        or quote.get("author") != author_to_delete
    ]

    if len(remaining_quotes) == len(quotes):
        return jsonify({"error": "Quote not found"}), 404

    quotes = remaining_quotes
    with open("quotes.json", "w") as f:
        json.dump(quotes, f)
    return jsonify({"message": "Quote deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
