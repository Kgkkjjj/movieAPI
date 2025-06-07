from fastapi import FastAPI, HTTPException
from data_loader import (
    get_movies,
    get_anime,
    get_movie,
    get_anime_item,
    search_movies,
    search_anime,
)

app = FastAPI(title="movieAPI")

@app.get("/movies")
def movies():
    return {"movies": get_movies()}


@app.get("/movies/search")
def movie_search(q: str):
    return {"movies": search_movies(q)}


@app.get("/movies/{movie_id}")
def movie_detail(movie_id: int):
    movie = get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/anime")
def anime():
    return {"anime": get_anime()}


@app.get("/anime/search")
def anime_search(q: str):
    return {"anime": search_anime(q)}


@app.get("/anime/{anime_id}")
def anime_detail(anime_id: int):
    show = get_anime_item(anime_id)
    if show is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return show
