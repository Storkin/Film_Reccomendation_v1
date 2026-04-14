from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

FILMS_FILE = "films.json"
USER_FILE = "user_data.json"


def load_films():
    try:
        with open(FILMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def load_user():
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"username": "Kullanıcı", "watched_films": {}}


def save_user(data):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/films")
def get_films():
    films = load_films()
    genre = request.args.get("genre", "").strip().lower()
    min_score = request.args.get("min_score", "").strip()
    year = request.args.get("year", "").strip()
    search = request.args.get("search", "").strip().lower()

    if genre:
        films = [f for f in films if any(genre in g.lower() for g in f.get("genres", []))]

    if min_score:
        try:
            ms = float(min_score)
            films = [f for f in films if f.get("score") and float(f["score"]) >= ms]
        except ValueError:
            pass

    if year:
        films = [f for f in films if str(f.get("release_year", "")) == year]

    if search:
        films = [f for f in films if search in f.get("title", "").lower() or
                 search in f.get("director", "").lower()]

    return jsonify(films)


@app.route("/api/genres")
def get_genres():
    films = load_films()
    genres = set()
    for film in films:
        for g in film.get("genres", []):
            genres.add(g.strip())
    return jsonify(sorted(genres))


@app.route("/api/years")
def get_years():
    films = load_films()
    years = sorted(set(str(f.get("release_year", "")) for f in films if f.get("release_year")), reverse=True)
    return jsonify(years)


@app.route("/api/user")
def get_user():
    return jsonify(load_user())


@app.route("/api/watch", methods=["POST"])
def mark_watched():
    data = request.json
    title = data.get("title")
    film_data = data.get("film")
    user = load_user()

    if title not in user["watched_films"]:
        user["watched_films"][title] = {
            "film": film_data,
            "rating": None,
            "review": None
        }
        save_user(user)
        return jsonify({"status": "added", "message": f"'{title}' izlendi olarak işaretlendi."})
    else:
        return jsonify({"status": "exists", "message": f"'{title}' zaten listede."})


@app.route("/api/unwatch", methods=["POST"])
def unmark_watched():
    data = request.json
    title = data.get("title")
    user = load_user()

    if title in user["watched_films"]:
        del user["watched_films"][title]
        save_user(user)
        return jsonify({"status": "removed", "message": f"'{title}' listeden çıkarıldı."})
    else:
        return jsonify({"status": "not_found", "message": f"'{title}' listede bulunamadı."})


@app.route("/api/review", methods=["POST"])
def add_review():
    data = request.json
    title = data.get("title")
    rating = data.get("rating")
    review = data.get("review", "")
    user = load_user()

    if title not in user["watched_films"]:
        return jsonify({"status": "error", "message": "Filmi önce izlendi olarak işaretleyin."}), 400

    try:
        rating = float(rating)
        if not (0 <= rating <= 10):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Puan 0-10 arasında olmalı."}), 400

    user["watched_films"][title]["rating"] = rating
    user["watched_films"][title]["review"] = review
    save_user(user)
    return jsonify({"status": "ok", "message": "Değerlendirme kaydedildi."})


if __name__ == "__main__":
    app.run(debug=True)
