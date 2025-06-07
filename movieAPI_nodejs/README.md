# movieAPI Node.js

A minimal Express server that mirrors the features of the Python `movieAPI`.
It fetches `movies.json` and `anime.json` from the upstream
[shows-](https://github.com/Kgkkjjj/shows-/tree/main) repository, caches the
results in memory, and exposes several endpoints.

## Endpoints

- `GET /movies` - List all movies.
- `GET /movies/:id` - Retrieve a movie by numeric ID.
- `GET /movies/search?q=` - Search movie titles.
- `GET /anime` - List all anime shows.
- `GET /anime/:id` - Retrieve an anime show by ID.
- `GET /anime/search?q=` - Search anime titles.
- `POST /refresh` - Force refresh of cached data.

## Running

Install dependencies and start the server:

```bash
cd movieAPI_nodejs
npm install
npm start
```

The server listens on port `3000` by default. Set the `PORT` environment
variable to change it.
