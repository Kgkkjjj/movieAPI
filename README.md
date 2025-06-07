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
- `/refresh` (POST) - Force refresh of cached data from GitHub.

The service caches movie and anime data in memory for five minutes to
avoid repeatedly hitting the upstream repository. Use `/refresh` if you need
to force an update immediately.

## Running

Install dependencies and start the server:

```bash
pip install fastapi uvicorn requests
uvicorn main:app --reload
```

## Node.js Version

For users that prefer Node.js, a companion implementation lives in
`movieAPI_nodejs/`. It exposes similar endpoints using Express.

Run it with:

```bash
cd movieAPI_nodejs
npm install
npm start
```

## GTK Movie Uploader

A simple C/GTK program in `gtk_uploader/` lets you append new entries to
`movies.json`. Build it with `make` (requires `gtk+-3.0`, `libcurl`, and
`jansson` development headers). Running the resulting `uploader` binary
provides a small form to submit new movie records. By default the updated
file is written locally, but you can adapt the program to upload it back to
GitHub using a personal access token in the `GITHUB_TOKEN` environment
variable.

## Updating `movies.json`

The repository includes a helper script `update_movies.py` that downloads
`movies.json` from the upstream repository and commits the updated file. If
you have the GPG key `9F28B4FCD2B9A0BE` available, the script attempts to
sign the commit. Usage:

```bash
python update_movies.py "Update movies.json"
```

If signing fails (e.g. the key is not present), the commit will be created
without a signature.
