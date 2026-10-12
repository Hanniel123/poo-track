from fastapi import FastAPI, HTTPException
import config
from handlers import *
from utils import *
from models import Artist

app = FastAPI()

@app.get('/api/festival')
def get_festival_info():
    data = parse_file(config.DATABASE_FILE)

    return {
        'name': data['name'],
        'first_day': data['first_day'],
        'last_day': data['last_day'],
        'days': get_festival_days(data['performances'])
    }

@app.get('/api/venues')
def get_venues():
    data = parse_file(config.DATABASE_FILE)
    return serialize_venues(data['venues'])

@app.get('/api/artists')
def get_artists():
    data = parse_file(config.DATABASE_FILE)

    artists = [Artist(artist).serialize() for artist in data['artists']]
    return sorted(artists, key=lambda a: a['slug'])

@app.get('/api/artists/{slug}')
def get_artist(slug: str):
    data = parse_file(config.DATABASE_FILE)
    artists: list[Artist] = [Artist(a) for a in data['artists']]

    result = [art for art in artists if art.slug == slug]
    if (len(result) != 1):
        raise HTTPException(status_code=404, detail="Artist not found")
    return result[0].serialize()
