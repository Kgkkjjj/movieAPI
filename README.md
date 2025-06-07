# movieAPI

A simple FastAPI application that attempts to fetch movie and anime show data
from [shows-](https://github.com/Kgkkjjj/shows-/tree/main). The remote
repository currently contains no actual show lists, so the API endpoints will
return empty arrays until data files (`movies.json` and `anime.json`) are added
to that repository.

## Endpoints

- `/movies` - Returns a list of movies from the remote repo.
- `/anime` - Returns a list of anime from the remote repo.

## Running

Install dependencies and start the server:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```
