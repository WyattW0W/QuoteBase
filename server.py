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
    new_quote = request.form.get("quote")
    if new_quote:
        quotes.append(new_quote)
        with open("quotes.json", "w") as f:
            json.dump(quotes, f)
        return redirect(url_for("get_quotes"))
    else:
        return "Quote cannot be empty", 400

if __name__ == "__main__":
    app.run(debug=True)
