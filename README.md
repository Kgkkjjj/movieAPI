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
- `/movies/count` - Total count of available movies.
- `/movies/stats` - Summary stats for movie file sizes.
- `/movies/sorted_by_size` - Movies sorted by file size.
- `/movies/sorted_by_episode` - Movies sorted by season/episode.
- `/movies/sorted_by_title` - Movies sorted alphabetically by title.
- `/movies/latest` - Retrieve the most recent movie.
- `/movies/by_season/{season}` - Movies within a season.
- `/movies/shows/{show}/season/{season}` - Movies for a show and season.
- `/movies/shows/{show}/episode/{episode}` - Movies for a show and episode.
- `/movies/random` - Retrieve a random movie.
- `/shows` - List all unique show names present in the movie dataset.
- `/shows/search?q=name` - Search show names.
- `/shows/{show}/seasons` - List seasons available for a show.
- `/shows/{show}/summary` - Map seasons to episode lists.
- `/shows/{show}/seasons/{season}/episodes` - List episodes for a specific season.
- `/anime` - Returns a list of anime from the remote repo.
- `/anime/count` - Total count of anime entries.
- `/anime/random` - Retrieve a random anime show.
- `/anime/sorted_by_title` - Anime shows sorted alphabetically by title.
- `/anime/latest` - Retrieve the last anime show in the list.
- `/anime/{id}` - Look up an anime show by numeric `id`.
- `/anime/search?q=title` - Search anime by title substring.

## Running

Install dependencies and start the server:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```
