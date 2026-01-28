import json 
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk, messagebox
        
class Film():
    HIGH_SCORE_THRESHOLD = 8
    def __init__(self, title, director=None, release_year=None, duration=None, score=None, 
                 genres=None, cast=None, language=None, description=None, ):
        self.title = title
        self.director = director
        self.release_year = release_year
        self.duration = duration
        self.score = score
        self.genres = genres if genres else []        
        self._cast = []             
        self.language = language
        self.description = description
        
    
    def make_comment(self):
        pass
        
    def __str__(self):
        return f"{self.title} ({', '.join(self.genres)}) - score: {self.score}"
    
    @property
    def cast(self):
        return self._cast
    
    @cast.setter
    def cast(self, value):
        raise AttributeError("Do not set cast directly. Use add_actor or add_actors methods.")
    
    def add_actor(self, actor_name):
        

        if actor_name not in self._cast:
            self._cast.append(actor_name)
            # print(f"{actor_name} succesfully added.")
        else:
            print(f"{actor_name} is already in the cast.")
        

    def remove_actor(self, actor_name):
        if actor_name in self._cast:
            self._cast.remove(actor_name)
        else:
            print(f"{actor_name} is not found in the cast.")


    def add_actors(self, actor_list):
        for actor in actor_list:
            self.add_actor(actor)

    def remove_actors(self, actor_list):
        for actor in actor_list:
            self.remove_actor(actor)

    def show_cast(self):
        if not self._cast:
            print("Cast list is empty.")
        else:
            print("🎭 Cast List:")
            for actor in self._cast:
                print(f"- {actor}")

    def display_details(self):
        print(f"Title:{self.title}")
        print(f"Director:{self.director}")
        print(f"Release year:{self.release_year}")
        print(f"Duration:{self.duration} minutes")
        print(f"IMDb Score:{self.score}")
        print(f"Genres: {', '.join(self.genres)}")
        print(f"Language:{self.language}")
        print(f"Cast:{', '.join(self.cast)}")
        print(f"Description:{self.description}")
    def is_highly_rated(self):
        if self.score is None:
            return "score not avaible"
        if self.score>self.HIGH_SCORE_THRESHOLD:
            return f"score of this film is {self.score} worthy to watch"
        else:
            return f"score of this film is {self.score} not worthy to watch"

    def update_score(self,new_score):
        if 0<=new_score<=10:
            self.score=new_score
            print("imdb score updated ")
        else:
            print("invalid score please enter score between 0-10.")

class Action(Film):
    def make_comment(self):
        if self.score >= 8:
            return  " a thrilling action-packed film, highly recommended for adrenaline lovers!"
        elif self.score >= 6:
            return " it  decent action sequences but might lack depth."
        else:
            return  " it falls short in delivering engaging action; consider other titles in the genre."
    
class Comedy(Film):
    def make_comment(self):
        if self.score >= 8:
            return "A clever and genuinely funny comedy. Worth your time."
        elif self.score >= 6:
            return "Light entertainment with a few good laughs."
        else:
            return "Fails to deliver consistent humor or engaging moments."

class Romance(Film):
    def make_comment(self):
        if self.score >= 8:
            return "A touching love story with strong emotional depth."
        elif self.score >= 6:
            return "Decent romantic elements, though not very memorable."
        else:
            return "Lacks chemistry and emotional engagement."

class Thriller(Film):
    def make_comment(self):
        if self.score >= 8:
            return "A gripping and intense thriller. Keeps you on the edge."
        elif self.score >= 6:
            return "Moderate tension with some predictable turns."
        else:
            return "Lacks suspense and fails to build real excitement."

class Horror(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Genuinely terrifying and atmospherically intense."
        elif self.score >= 6:
            return "Has a few scares, but not consistently frightening."
        else:
            return "Fails to create fear or tension effectively."

class Science_Fiction(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Thought-provoking and visually imaginative sci-fi."
        elif self.score >= 6:
            return "Some good ideas, but lacks depth or coherence."
        else:
            return "Weak execution of sci-fi concepts."

class Fantasy(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Enchanting world-building and immersive storytelling."
        elif self.score >= 6:
            return "Interesting visuals but the story feels shallow."
        else:
            return "Fails to create a convincing fantasy universe."

class Documentary(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Informative, compelling, and well-researched."
        elif self.score >= 6:
            return "Some insightful content but not very engaging."
        else:
            return "Lacks depth and fails to present facts effectively."

class Animation(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Beautifully crafted with emotional storytelling."
        elif self.score >= 6:
            return "Decent visuals, but not very impactful."
        else:
            return "Poor animation quality or weak narrative."

class Adventure(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Exciting journey with strong pacing and action."
        elif self.score >= 6:
            return "Offers mild adventure with occasional thrills."
        else:
            return "Fails to deliver a compelling sense of exploration."

class Crime(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Well-crafted with layered characters and tension."
        elif self.score >= 6:
            return "Serviceable crime plot, though lacking depth."
        else:
            return "Unconvincing and underdeveloped narrative."

class Mystery(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Intricate and engaging, a rewarding mystery experience."
        elif self.score >= 6:
            return "Mildly interesting with some predictable twists."
        else:
            return "Fails to build suspense or maintain curiosity."

class Musical(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Vibrant, energetic, and emotionally expressive."
        elif self.score >= 6:
            return "Entertaining but lacks musical or narrative depth."
        else:
            return "Forgets to balance story with music effectively."

class Biography(Film):
    def make_comment(self):
        if self.score >= 8:
            return "Insightful and emotionally powerful portrayal."
        elif self.score >= 6:
            return "Provides general information, but not very compelling."
        else:
            return "Misses the essence of the subject’s life story."

class User:
    def __init__(self,username):
        self.username=username
        self.watched_films = {}

    def mark_as_watched(self,film):
        if film.title not in self.watched_films:
            self.watched_films[film.title] = {"film": film}
            print(f"{film.title} marked as watched. ")
        else:
            print(f"{film.title} is already marked as watched. ")
    def remove_watched_film(self,film):
        if film.title in self.watched_films:
            del self.watched_films[film.title]
            print(f"'{film.title}' has been removed from your watched films.")
        else:
            print(f"'{film.title}' is not in your watched list.")  
     
    def show_watched_films(self):
        if not  self.watched_films:
            print("no films in the list yet")
        else:
            print(f"\n {self.username}'s watched films:")
            for title,data in self.watched_films.items():
                print(f"- {title}")


    def review_and_rating(self, title,rating,review):
        if title not in self.watched_films:
            print(" You need to mark the film as watched first.")
            return
        
        if not (0 <= rating <= 10):
            raise ValueError(" Rating must be between 0 and 5.")

        
        self.watched_films[title]["rating"] = rating
        self.watched_films[title]["review"] = review
        print(f" Review and rating for '{title}' saved.")
    def show_reviews(self):
        if not self.watched_films:
            print(" You have not reviewed any films yet.")
        else:
            print(f"\n {self.username}'s Film Reviews:")
            for title, data in self.watched_films.items():
                rating = data.get("rating", "N/A")
                review = data.get("review", "No review")
                print(f"\n {title}")
                print(f" Rating: {rating}")
                print(f" Review: {review}")

class FilmGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Film Filtreleme")

        # Species selection
        tk.Label(self.root, text="Tür:").grid(row=0, column=0, sticky="w")
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=0, column=1)

        # Minimum score selection
        tk.Label(self.root, text="Minimum Puan:").grid(row=1, column=0, sticky="w")
        self.score_entry = tk.Entry(self.root)
        self.score_entry.grid(row=1, column=1)

        # Year selection
        tk.Label(self.root, text="Yıl:").grid(row=2, column=0, sticky="w")
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1)

        # Button filters
        self.filter_btn = tk.Button(self.root, text="Filtrele", command=self.filter_films)
        self.filter_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Result list
        self.result_list = tk.Listbox(self.root, width=60, height=20)
        self.result_list.grid(row=4, column=0, columnspan=2)

        self.root.mainloop()

    def filter_films(self):
        genre = self.genre_entry.get().strip()
        score = self.score_entry.get().strip()
        year = self.year_entry.get().strip()

        filtered = self.manager.films

        if genre:
            filtered = self.manager.filter_by_genre(genre)

        if score:
            try:
                min_score = float(score)
                filtered = [f for f in filtered if f.score and f.score >= min_score]
            except ValueError:
                messagebox.showerror("Hata", "Puan sayısal bir değer olmalı.")
                return

        if year:
            filtered = [f for f in filtered if f.release_year and str(f.release_year) == year]

        self.result_list.delete(0, tk.END)
        if not filtered:
            self.result_list.insert(tk.END, "Filtreye uygun film bulunamadı.")
        else:
            for film in filtered:
                self.result_list.insert(tk.END, str(film))

    
def load_films(filename="films.json"):
    try:
        with open(filename,"r",encoding="utf-8") as f:
            data=json.load(f)
            films=[]
            for item in data:
                film=Film(title=item["title"],
                    director=item.get("director"),
                    release_year=item.get("release_year"),
                    duration=item.get("duration"),
                    score=item.get("score"),
                    genres=item.get("genres"),
                    cast=item.get("cast"),
                    language=item.get("language"),
                    description=item.get("description"))
                film.add_actors(item.get("cast",[]))
                films.append(film)
            return films  
    except FileNotFoundError:
        return []

def save_user(user, filename="user_data.json"):
    data = {
        "username": user.username,
        "watched_films": {}
    }

    for title, details in user.watched_films.items():
        film = details["film"]
        data["watched_films"][title] = {
            "rating": details.get("rating"),
            "review": details.get("review"),
            "film": {
                "title": film.title,
                "director": film.director,
                "release_year": film.release_year,
                "duration": film.duration,
                "score": film.score,
                "genres": film.genres,
                "cast": film.cast,
                "language": film.language,
                "description": film.description
            }
        }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(" User data saved.")

def load_user(filename="user_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(" No user data found.")
        return None

    user = User(data["username"])
    
    for title, details in data["watched_films"].items():
        film_data = details["film"]
        film = Film(
            title=film_data["title"],
            director=film_data.get("director"),
            release_year=film_data.get("release_year"),
            duration=film_data.get("duration"),
            score=film_data.get("score"),
            genres=film_data.get("genres"),
            language=film_data.get("language"),
            description=film_data.get("description")
        )
        film.add_actors(film_data.get("cast", []))

        user.watched_films[title] = {
            "film": film,
            "rating": details.get("rating"),
            "review": details.get("review")
        }

    print(" User data loaded.")
    return user

class FilmManager:
    def __init__(self, films=None):
        self.films = films if films else []

    def add_film(self, film):
        self.films.append(film)

    def filter_by_genre(self, genre):
        return [film for film in self.films if genre.lower() in (g.lower() for g in film.genres)]

    def filter_by_score(self, min_score):
        return [film for film in self.films if film.score and film.score >= min_score]

    def filter_by_year(self, year):
        return [film for film in self.films if film.release_year and str(film.release_year) == str(year)]

    def list_films(self, films=None):
        films_to_list = films if films is not None else self.films
        if not films_to_list:
            print("No films found with the given filter.")
            return
        for film in films_to_list:
            print(film)


    



cast_columns = ['Star1', 'Star2', 'Star3', 'Star4']  
def get_cast_from_row(row):
    cast_list = []
    for col in cast_columns:
        actor = row.get(col)
        if isinstance(actor, str) and actor.strip():
            cast_list.append(actor.strip())
    return cast_list

def convert_csv_to_film_objects(df):
    films = []

    for _, row in df.iterrows():
        title = row.get("Series_Title")
        director = row.get("Director", None)
        release_year = row.get("Released_Year", None)
        
        # Convert runtime to minutes (example: "142 min")
        runtime_raw = row.get("Runtime", "")
        duration = None
        if isinstance(runtime_raw, str) and runtime_raw.endswith("min"):
            try:
                duration = int(runtime_raw.replace("min", "").strip())
            except ValueError:
                duration = None

        score = row.get("IMDB_Rating", None)
        genres = row.get("Genre", "").split(",") if isinstance(row.get("Genre"), str) else []
        description = row.get("Overview", "...")
        language = "English"  # Constant language 

        film = Film(
            title=title,
            director=director,
            release_year=release_year,
            duration=duration,
            score=score,
            genres=genres,
            language=language,
            description=description,
        )

        
        cast_columns = ["Star1", "Star2", "Star3", "Star4"]
        cast_list = []
        for col in cast_columns:
            actor = row.get(col)
            if isinstance(actor, str) and actor.strip():
                cast_list.append(actor.strip())

        film.add_actors(cast_list)
        films.append(film)

    return films



def save_to_json(films, filename="films.json"):
    data = []
    for film in films:
        data.append({
            "title": film.title,
            "director": film.director,
            "release_year": film.release_year,
            "duration": film.duration,
            "score": film.score,
            "genres": film.genres,
            "cast": film.cast,
            "language": film.language,
            "description": film.description
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(" Film data saved in JSON file.")


if __name__ == "__main__":
    movies_df = pd.read_csv("imdb_top_1000.csv")
    films = convert_csv_to_film_objects(movies_df)
    save_to_json(films)
    films = load_films("films.json")

    manager = FilmManager(films)

    FilmGUI(manager)