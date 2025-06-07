from fastapi import FastAPI, HTTPException
from data_loader import (
    get_movies,
    get_anime,
    get_movie,
    get_anime_item,
    search_movies,
    search_anime,
    filter_movies_by_size,
    get_movies_by_show,
    get_unique_shows,
    get_seasons_for_show,
    get_episodes_for_show_season,
    # new helpers
    get_movie_count,
    get_movie_stats,
    sort_movies_by_size,
    sort_movies_by_episode,
    filter_movies_by_season,
    filter_movies_by_show_season,
    filter_movies_by_show_episode,
    get_random_movie,
    get_random_anime,
    search_shows,
    get_show_summary,
    get_anime_count,
)

app = FastAPI(title="movieAPI")

@app.get("/movies")
def movies():
    return {"movies": get_movies()}


@app.get("/movies/count")
def movie_count():
    """Return total number of movies."""
    return {"count": get_movie_count()}


@app.get("/movies/stats")
def movie_stats():
    """Return aggregate statistics about movie file sizes."""
    return get_movie_stats()


@app.get("/movies/sorted_by_size")
def movies_sorted_by_size(order: str = "asc"):
    """Return movies sorted by file size."""
    return {"movies": sort_movies_by_size(order)}


@app.get("/movies/sorted_by_episode")
def movies_sorted_by_episode(order: str = "asc"):
    """Return movies sorted by season/episode order."""
    return {"movies": sort_movies_by_episode(order)}


@app.get("/movies/by_season/{season}")
def movies_by_season(season: int):
    """Return all movies in a given season."""
    return {"movies": filter_movies_by_season(season)}


@app.get("/movies/shows/{show}/season/{season}")
def movies_show_season(show: str, season: int):
    """Movies for a show filtered by season."""
    return {"movies": filter_movies_by_show_season(show, season)}


@app.get("/movies/shows/{show}/episode/{episode}")
def movies_show_episode(show: str, episode: int):
    """Movies for a show filtered by episode."""
    return {"movies": filter_movies_by_show_episode(show, episode)}


@app.get("/movies/random")
def movie_random():
    """Return a random movie."""
    movie = get_random_movie()
    if movie is None:
        raise HTTPException(status_code=404, detail="No movies available")
    return movie


@app.get("/movies/search")
def movie_search(q: str):
    return {"movies": search_movies(q)}


@app.get("/movies/by_size")
def movie_by_size(min: float = 0.0, max: float = 1e9):
    """Filter movies by file size in MB."""
    return {"movies": filter_movies_by_size(min, max)}


@app.get("/movies/shows/{show}")
def movies_for_show(show: str):
    """Return all movies belonging to a given show name."""
    return {"movies": get_movies_by_show(show)}


@app.get("/shows/search")
def shows_search(q: str):
    """Search available show names."""
    return {"shows": search_shows(q)}


@app.get("/shows")
def list_shows():
    """List unique show names."""
    return {"shows": get_unique_shows()}


@app.get("/shows/{show}/seasons")
def show_seasons(show: str):
    """List seasons available for a given show."""
    return {"seasons": get_seasons_for_show(show)}


@app.get("/shows/{show}/summary")
def show_summary(show: str):
    """Return mapping of seasons to episodes for a show."""
    return {"summary": get_show_summary(show)}


@app.get("/shows/{show}/seasons/{season}/episodes")
def show_episodes(show: str, season: int):
    """List episodes for a specific show and season."""
    return {"episodes": get_episodes_for_show_season(show, season)}


@app.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    movie = get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/anime")
def anime():
    return {"anime": get_anime()}


@app.get("/anime/count")
def anime_count():
    """Return number of anime shows."""
    return {"count": get_anime_count()}


@app.get("/anime/random")
def anime_random():
    """Return a random anime show."""
    show = get_random_anime()
    if show is None:
        raise HTTPException(status_code=404, detail="No anime available")
    return show


@app.get("/anime/search")
def anime_search(q: str):
    return {"anime": search_anime(q)}


@app.get("/anime/{anime_id}")
def anime_detail(anime_id: int):
    show = get_anime_item(anime_id)
    if show is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return show
