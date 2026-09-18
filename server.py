from flask import Flask, request, jsonify, redirect, url_for, render_template
import json
from waitress import serve

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

@app.route("/quotes/edit-quote-template", methods=["GET"])
def edit_quote_template():
    quote_text = request.args.get("text")
    quote_author = request.args.get("author")
    return render_template("edit-quote.html", text=quote_text, author=quote_author), 200

@app.route("/quotes/edit-quote", methods=["POST"])
def edit_quote():
    global quotes

    quote_data = request.get_json(silent=True) or {}
    original_text = quote_data.get("original_text")
    original_author = quote_data.get("original_author")
    new_text = quote_data.get("new_text")
    new_author = quote_data.get("new_author")

    if not original_text or not original_author or not new_text or not new_author:
        return jsonify({"error": "All fields are required"}), 400

    for quote in quotes:
        if quote.get("text") == original_text and quote.get("author") == original_author:
            quote["text"] = new_text
            quote["author"] = new_author
            with open("quotes.json", "w") as f:
                json.dump(quotes, f)
            return jsonify({"message": "Quote updated successfully!"}), 200

    return jsonify({"error": "Original quote not found"}), 404

print("1. Script loaded successfully.")

if __name__ == "__main__":
    print("2. Starting the server on port 8000...")
    serve(app, host="0.0.0.0", port=8000)
