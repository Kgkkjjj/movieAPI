import json
import requests
from typing import List, Optional

REPO_BASE_URL = 'https://raw.githubusercontent.com/Kgkkjjj/shows-/main/'
MOVIES_FILE = 'movies.json'
ANIME_FILE = 'anime.json'


def fetch_remote_json(filename: str) -> List[dict]:
    url = REPO_BASE_URL + filename
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        # If the file isn't found or can't be parsed, return empty list
        return []


def get_movies() -> List[dict]:
    return fetch_remote_json(MOVIES_FILE)


def get_anime() -> List[dict]:
    return fetch_remote_json(ANIME_FILE)


def get_movie(movie_id: int) -> Optional[dict]:
    """Return a single movie by ID or None if not found."""
    for movie in get_movies():
        if movie.get("id") == movie_id:
            return movie
    return None


def get_anime_item(anime_id: int) -> Optional[dict]:
    """Return a single anime by ID or None if not found."""
    for show in get_anime():
        if show.get("id") == anime_id:
            return show
    return None


def search_movies(title: str) -> List[dict]:
    """Simple case-insensitive search by title substring."""
    query = title.lower()
    return [m for m in get_movies() if query in str(m.get("title", "")).lower()]


def search_anime(title: str) -> List[dict]:
    query = title.lower()
    return [a for a in get_anime() if query in str(a.get("title", "")).lower()]
