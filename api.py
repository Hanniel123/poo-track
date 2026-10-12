from fastapi import FastAPI, HTTPException
import config
from handlers import *
from utils import *
from models import Artist, Performance

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


@app.get('/api/programme')
def get_program(day: str | None=None, venue: str | None=None):
    data = parse_file(config.DATABASE_FILE)
    performances: list[dict] = data['performances']
    perfs = sorted([Performance(performance).serialize() for performance in performances], key=lambda a: a['festival_day'])
    if (day):
        perfs = [perf for perf in perfs if perf['festival_day'] == day]

    if (venue):
        perfs = [perf for perf in perfs if perf['venue'] == venue]

    return perfs

@app.get('/api/performances/{id}')
def get_performance(id: str):
    data = parse_file(config.DATABASE_FILE)
    performances: list[Performance] =[Performance(performance) for performance in data['performances']]
    result = [performance for performance in performances if performance.id == id]
    if (len(result) == 0):
        raise HTTPException(status_code=404, detail="Performance not found")
    return result[0].serialize()

@app.get('/api/now')
def now(at: str=datetime.now().isoformat(timespec='minutes')):
    at_date = datetime.fromisoformat(at)
    data = parse_file(config.DATABASE_FILE)
    performances: list[Performance] =[Performance(performance) for performance in data['performances']]
    on_stage: list[Performance] = []
    up_next: list[Performance] = []

    for performance in performances:
        if (at_date >= datetime.fromisoformat(performance.start) and at_date < datetime.fromisoformat(performance.end)):
            on_stage.append(performance)
        if (at_date >= datetime.fromisoformat(performance.end) and len(up_next) < 3):
            up_next.append(performance)
    return {
        'at': at,
        'now_playing': [p.serialize() for p in on_stage],
        'up_next': [p.serialize() for p in up_next]
    }


# Serve frontend
app.frontend('/', directory='web/public/')
app.frontend('/admin', directory='web/admin/')