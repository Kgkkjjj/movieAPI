from fastapi import FastAPI
from data_loader import get_movies, get_anime

app = FastAPI(title="movieAPI")

@app.get("/movies")
def movies():
    return {"movies": get_movies()}

@app.get("/anime")
def anime():
    return {"anime": get_anime()}
