# movieAPI

A small FastAPI service that fetches movie and anime data from the
[shows-](https://github.com/Kgkkjjj/shows-/tree/main) repository. The remote
repository does not currently provide real data, so responses are empty until
`movies.json` and `anime.json` are published there. As of this writing
[`movies.json`](https://github.com/Kgkkjjj/shows-/blob/main/movies.json)
contains eight episodes of the show **Wednesday**, each with a file size.
The API assigns sequential IDs when loading this data.

In addition to basic list endpoints, this API offers simple lookup and search
functionality similar to larger movie databases.

## Endpoints

- `/movies` - Returns a list of movies from the remote repo.
- `/movies/{id}` - Look up a movie by numeric `id`.
- `/movies/search?q=title` - Search movies by title substring.
- `/movies/by_size?min=&max=` - Filter movies by file size in MB.
- `/movies/shows/{show}` - List all movies for a particular show name.
- `/anime` - Returns a list of anime from the remote repo.
- `/anime/{id}` - Look up an anime show by numeric `id`.
- `/anime/search?q=title` - Search anime by title substring.

## Running

Install dependencies and start the server:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```
