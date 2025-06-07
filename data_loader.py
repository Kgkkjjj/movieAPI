import json
import requests
from typing import List, Optional
import re

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


def _parse_title(title: str):
    """Extract show name, season and episode from a title string."""
    m = re.search(r"^(?P<show>[^.]+)\.S(?P<season>\d+)E(?P<episode>\d+)", title)
    if m:
        return m.group("show"), int(m.group("season")), int(m.group("episode"))
    return None, None, None


def get_movies() -> List[dict]:
    """Return list of movies enriched with ids and parsed fields."""
    raw = fetch_remote_json(MOVIES_FILE)
    movies = []
    for idx, item in enumerate(raw, 1):
        show, season, episode = _parse_title(item.get("title", ""))
        movies.append(
            {
                "id": idx,
                "title": item.get("title"),
                "path": item.get("path"),
                "size_mb": item.get("size_mb"),
                "show": show,
                "season": season,
                "episode": episode,
            }
        )
    return movies


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


def filter_movies_by_size(min_size: float, max_size: float) -> List[dict]:
    """Return movies within a size range in megabytes."""
    return [
        m
        for m in get_movies()
        if m.get("size_mb") is not None and min_size <= float(m["size_mb"]) <= max_size
    ]


def get_movies_by_show(show_name: str) -> List[dict]:
    """Return all movies that match a show name (case-insensitive)."""
    query = show_name.lower()
    return [m for m in get_movies() if m.get("show", "").lower() == query]


def search_anime(title: str) -> List[dict]:
    query = title.lower()
    return [a for a in get_anime() if query in str(a.get("title", "")).lower()]
