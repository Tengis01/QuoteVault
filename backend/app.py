from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import sqlite3
import os
import random

app = Flask(__name__)
CORS(app)  # Бүх route-д CORS идэвхжүүлэх

def get_db_connection():
    db_type = os.getenv("MYSQL_HOST", "db")
    if db_type == "sqlite":
        return sqlite3.connect(os.getenv("MYSQL_DATABASE", "quotesdb"))
    else:
        return mysql.connector.connect(
            host=db_type,
            user=os.getenv("MYSQL_USER", "user"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            database=os.getenv("MYSQL_DATABASE", "quotesdb")
        )

@app.route('/quotes', methods=['GET'])
def get_quotes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if os.getenv("MYSQL_HOST", "db") != "sqlite" else conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    quotes = cursor.fetchall()
    if os.getenv("MYSQL_HOST", "db") == "sqlite":
        # SQLite-д dictionary хэлбэрээр хөрвүүлэх
        quotes = [{"id": row[0], "author": row[1], "quote": row[2]} for row in quotes]
    cursor.close()
    conn.close()
    return jsonify(quotes)

@app.route('/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    author = data.get("author")
    quote = data.get("quote")
    if not author or not quote:
        return jsonify({"message": "Author and quote are required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotes (author, quote) VALUES (%s, %s)" if os.getenv("MYSQL_HOST", "db") != "sqlite" else "INSERT INTO quotes (author, quote) VALUES (?, ?)", 
                  (author, quote))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Quote added"}), 201

@app.route('/quotes/random', methods=['GET'])
def get_random_quote():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) if os.getenv("MYSQL_HOST", "db") != "sqlite" else conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    quotes = cursor.fetchall()
    if os.getenv("MYSQL_HOST", "db") == "sqlite":
        quotes = [{"id": row[0], "author": row[1], "quote": row[2]} for row in quotes]
    cursor.close()
    conn.close()

    if not quotes:
        return jsonify({"message": "No quotes found"}), 404

    random_quote = random.choice(quotes)
    return jsonify(random_quote)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)