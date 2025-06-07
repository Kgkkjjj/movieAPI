import json
import requests
from typing import List

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
