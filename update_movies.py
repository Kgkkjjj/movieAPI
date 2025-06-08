import json
import requests
import subprocess
import sys
from pathlib import Path

REMOTE_URL = "https://raw.githubusercontent.com/Kgkkjjj/shows-/main/movies.json"
LOCAL_PATH = Path("movies.json")
GPG_KEY_ID = "9F28B4FCD2B9A0BE"


def fetch_remote_movies():
    resp = requests.get(REMOTE_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()


def save_movies(data):
    with LOCAL_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def git_commit(message: str):
    subprocess.run(["git", "add", str(LOCAL_PATH)], check=True)
    try:
        subprocess.run(
            [
                "git",
                "commit",
                "-S",
                f"--gpg-sign={GPG_KEY_ID}",
                "-m",
                message,
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        # Fall back to unsigned commit if signing fails
        subprocess.run(["git", "commit", "-m", message], check=True)


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "Update movies.json"
    data = fetch_remote_movies()
    save_movies(data)
    git_commit(message)


if __name__ == "__main__":
    main()
