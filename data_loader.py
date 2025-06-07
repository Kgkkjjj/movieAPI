import json
import requests
from typing import List, Optional
import re
import random

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


def get_unique_shows() -> List[str]:
    """Return a sorted list of unique show names present in the movies."""
    shows = {m["show"] for m in get_movies() if m.get("show")}
    return sorted(shows)


def get_seasons_for_show(show_name: str) -> List[int]:
    """Return a sorted list of seasons for a given show."""
    query = show_name.lower()
    seasons = {m["season"] for m in get_movies() if m.get("show", "").lower() == query and m.get("season") is not None}
    return sorted(seasons)


def get_episodes_for_show_season(show_name: str, season: int) -> List[dict]:
    """Return movies that match a show name and season number."""
    query = show_name.lower()
    return [
        m
        for m in get_movies()
        if m.get("show", "").lower() == query and m.get("season") == season
    ]


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


# Additional helper systems
def get_movie_count() -> int:
    """Return the total number of movies available."""
    return len(get_movies())


def get_movie_stats() -> dict:
    """Return simple statistics about movie sizes."""
    movies = get_movies()
    sizes = [float(m["size_mb"]) for m in movies if m.get("size_mb") is not None]
    total = sum(sizes)
    avg = total / len(sizes) if sizes else 0.0
    return {"count": len(movies), "total_size_mb": total, "avg_size_mb": avg}


def sort_movies_by_size(order: str = "asc") -> List[dict]:
    """Return movies sorted by file size."""
    movies = sorted(
        get_movies(), key=lambda m: (m.get("size_mb") is None, m.get("size_mb", 0.0))
    )
    if order == "desc":
        movies.reverse()
    return movies


def sort_movies_by_episode(order: str = "asc") -> List[dict]:
    """Return movies sorted by season/episode."""
    movies = sorted(
        get_movies(), key=lambda m: (m.get("season", 0), m.get("episode", 0))
    )
    if order == "desc":
        movies.reverse()
    return movies


def sort_movies_by_title(order: str = "asc") -> List[dict]:
    """Return movies sorted by title."""
    movies = sorted(get_movies(), key=lambda m: m.get("title", ""))
    if order == "desc":
        movies.reverse()
    return movies


def filter_movies_by_season(season: int) -> List[dict]:
    """Return all movies for a given season number."""
    return [m for m in get_movies() if m.get("season") == season]


def filter_movies_by_show_season(show: str, season: int) -> List[dict]:
    """Return movies for a show filtered by season."""
    query = show.lower()
    return [
        m
        for m in get_movies()
        if m.get("show", "").lower() == query and m.get("season") == season
    ]


def filter_movies_by_show_episode(show: str, episode: int) -> List[dict]:
    """Return movies for a show filtered by episode number."""
    query = show.lower()
    return [
        m
        for m in get_movies()
        if m.get("show", "").lower() == query and m.get("episode") == episode
    ]


def get_random_movie() -> Optional[dict]:
    """Return a random movie if available."""
    movies = get_movies()
    return random.choice(movies) if movies else None


def get_random_anime() -> Optional[dict]:
    """Return a random anime show if available."""
    shows = get_anime()
    return random.choice(shows) if shows else None


def search_shows(query: str) -> List[str]:
    """Case-insensitive search across available show names."""
    q = query.lower()
    return [s for s in get_unique_shows() if q in s.lower()]


def get_show_summary(show: str) -> dict:
    """Return mapping of seasons to episode numbers for a show."""
    episodes = get_movies_by_show(show)
    summary = {}
    for m in episodes:
        season = m.get("season")
        ep = m.get("episode")
        if season is None or ep is None:
            continue
        summary.setdefault(season, []).append(ep)
    for season in summary:
        summary[season] = sorted(summary[season])
    return {k: summary[k] for k in sorted(summary)}


def get_anime_count() -> int:
    """Return the number of anime shows available."""
    return len(get_anime())


def get_latest_movie() -> Optional[dict]:
    """Return the movie with the highest season/episode."""
    movies = sort_movies_by_episode(order="desc")
    return movies[0] if movies else None


def get_latest_anime() -> Optional[dict]:
    """Return the last anime show in the list if available."""
    shows = get_anime()
    return shows[-1] if shows else None


def sort_anime_by_title(order: str = "asc") -> List[dict]:
    """Return anime shows sorted alphabetically by title."""
    shows = sorted(get_anime(), key=lambda a: a.get("title", ""))
    if order == "desc":
        shows.reverse()
    return shows

