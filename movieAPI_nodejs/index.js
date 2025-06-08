const express = require('express');

const REPO_BASE_URL = 'https://raw.githubusercontent.com/Kgkkjjj/shows-/main/';
const MOVIES_FILE = 'movies.json';
const ANIME_FILE = 'anime.json';

let moviesCache = [];
let animeCache = [];
let moviesCacheTime = 0;
let animeCacheTime = 0;
const CACHE_TTL = 300; // seconds

async function fetchJson(file) {
  try {
    const res = await fetch(REPO_BASE_URL + file, { timeout: 5000 });
    if (!res.ok) {
      return [];
    }
    return await res.json();
  } catch (err) {
    return [];
  }
}

function parseTitle(title) {
  const m = /^(?<show>[^.]+)\.S(?<season>\d+)E(?<episode>\d+)/i.exec(title);
  if (m && m.groups) {
    return [m.groups.show, parseInt(m.groups.season), parseInt(m.groups.episode)];
  }
  return [null, null, null];
}

async function getMovies(force = false) {
  const now = Date.now() / 1000;
  if (!force && moviesCache.length && now - moviesCacheTime < CACHE_TTL) {
    return moviesCache;
  }
  const raw = await fetchJson(MOVIES_FILE);
  moviesCache = raw.map((item, idx) => {
    const [show, season, episode] = parseTitle(item.title || '');
    return {
      id: idx + 1,
      title: item.title,
      path: item.path,
      size_mb: item.size_mb,
      show,
      season,
      episode,
    };
  });
  moviesCacheTime = now;
  return moviesCache;
}

async function getAnime(force = false) {
  const now = Date.now() / 1000;
  if (!force && animeCache.length && now - animeCacheTime < CACHE_TTL) {
    return animeCache;
  }
  const raw = await fetchJson(ANIME_FILE);
  animeCache = raw.map((item, idx) => ({ id: idx + 1, ...item }));
  animeCacheTime = now;
  return animeCache;
}

async function getMovie(id) {
  const movies = await getMovies();
  return movies.find((m) => m.id === id) || null;
}

async function getAnimeItem(id) {
  const shows = await getAnime();
  return shows.find((a) => a.id === id) || null;
}

async function searchMovies(query) {
  const q = query.toLowerCase();
  const movies = await getMovies();
  return movies.filter((m) => m.title && m.title.toLowerCase().includes(q));
}

async function searchAnime(query) {
  const q = query.toLowerCase();
  const shows = await getAnime();
  return shows.filter((a) => a.title && a.title.toLowerCase().includes(q));
}

async function refreshCache() {
  await getMovies(true);
  await getAnime(true);
  return { movies: moviesCache.length, anime: animeCache.length };
}

const app = express();

app.get('/movies', async (_req, res) => {
  res.json({ movies: await getMovies() });
});

app.get('/movies/search', async (req, res) => {
  const q = req.query.q || '';
  res.json({ movies: await searchMovies(String(q)) });
});

app.get('/movies/:id', async (req, res) => {
  const movie = await getMovie(parseInt(req.params.id, 10));
  if (!movie) {
    res.status(404).json({ detail: 'Movie not found' });
  } else {
    res.json(movie);
  }
});

app.get('/anime', async (_req, res) => {
  res.json({ anime: await getAnime() });
});

app.get('/anime/search', async (req, res) => {
  const q = req.query.q || '';
  res.json({ anime: await searchAnime(String(q)) });
});

app.get('/anime/:id', async (req, res) => {
  const show = await getAnimeItem(parseInt(req.params.id, 10));
  if (!show) {
    res.status(404).json({ detail: 'Anime not found' });
  } else {
    res.json(show);
  }
});

app.post('/refresh', async (_req, res) => {
  res.json(await refreshCache());
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`movieAPI Node.js listening on ${PORT}`);
});
