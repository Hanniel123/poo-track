from fastapi import FastAPI, HTTPException, Response, status
from handlers import *
from utils import *
from models import Artist, Performance, Venue
from storage import Storage
from request_models import *
from dateutil.parser import parse

app = FastAPI()
storage = Storage()


###### GET METHODS

@app.get('/api/festival')
def get_festival_info():
    data = storage.data()

    return {
        'name': data['name'],
        'first_day': data['first_day'],
        'last_day': data['last_day'],
        'days': get_festival_days(data['performances'])
    }

@app.get('/api/venues')
def get_venues():
    data = storage.data()
    return [Venue(venue).serialize() for venue in data['venues']]

@app.get('/api/artists')
def get_artists():
    data = storage.data()

    artists = [Artist(artist).serialize() for artist in data['artists']]
    return sorted(artists, key=lambda a: a['slug'])

@app.get('/api/artists/{slug}')
def get_artist(slug: str):
    data = storage.data()
    artists: list[Artist] = [Artist(a) for a in data['artists']]

    result = [art for art in artists if art.slug == slug]
    if (len(result) != 1):
        raise HTTPException(status_code=404, detail="Artist not found")
    return result[0].serialize()


@app.get('/api/programme')
def get_program(day: str | None=None, venue: str | None=None):
    data = storage.data()
    performances: list[dict] = data['performances']
    perfs = sorted([Performance(performance).serialize() for performance in performances], key=lambda a: a['festival_day'])
    if (day):
        perfs = [perf for perf in perfs if perf['festival_day'] == day]

    if (venue):
        perfs = [perf for perf in perfs if perf['venue'] == venue]

    return perfs

@app.get('/api/performances/{id}')
def get_performance(id: str):
    data = storage.data()
    performances: list[Performance] =[Performance(performance) for performance in data['performances']]
    result = [performance for performance in performances if performance.id == id]
    if (len(result) == 0):
        raise HTTPException(status_code=404, detail="Performance not found")
    return result[0].serialize()

@app.get('/api/now')
def now(at: str=datetime.now().isoformat(timespec='minutes')):
    at_date = datetime.fromisoformat(at)
    data = storage.data()
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


##### WRITE METHODS
@app.post('/api/artists')
def add_artist(artist: ArtistModel, response: Response):
    """
    Add one artist to the festival
    """
    data = storage.data()
    data['artists'].append(artist.model_dump())
    try:
        storage.update(data)
        response.status_code = status.HTTP_201_CREATED
        return artist.model_dump()
    except:
        raise HTTPException(500, detail="Failed to update database")


@app.post('/api/performances')
def add_performance(performance: PerformanceModel, response: Response):
    data = storage.data()

    # Check venu
    venues: list[Venue]  = [Venue(venue) for venue in data['venues']]

    found_venue: None | Venue = None
    for v in venues:
        if (v.slug == performance.venue):
            found_venue = v
    if (not found_venue):
        raise HTTPException(404, detail="Invalid venue")

    # Check date format
    if (not parse(performance.start)):
        raise HTTPException(422, detail="Invalid date format")

    all_acts = [Artist(artist).slug for artist in data['artists']]
    perf: None | dict = None
    # Check by case
    match (performance.kind):
        case 'lineup':
            if (not performance.host or not performance.acts):
                raise HTTPException(422, detail="host and acts fields required for lineup kind")
            # Verify host and acts
            for act in performance.acts:
                if (not (act in all_acts)):
                    raise HTTPException(404, detail="Invalid act")
            if (not (performance.host in all_acts)):
                raise HTTPException(404, detail="Invalid act")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'host': performance.host,
                'acts': performance.acts
            }
        case 'solo':
            if (not performance.min_age or not performance.artist):
                raise HTTPException(422, detail="min_age and artist field required for solo kind")
            if (performance.min_age < 0):
                raise HTTPException(422, detail="Invalid min_age field")
            if (not (performance.artist in all_acts)):
                raise HTTPException(404, detail="Invalid artist field")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'artist': performance.artist,
                'min_age': performance.min_age
            }
        case 'workshop':
            if ((not performance.teacher) or (not performance.max_participants) or (not performance.participants)):
                raise HTTPException(422, detail="teacher, max_participants and participants fields are required")
            if (not (performance.teacher in all_acts)):
                raise HTTPException(404, detail="Invalid teacher")
            if (performance.max_participants == 0):
                raise HTTPException(422, detail="max_participants field must be positive")
            if (len(performance.participants) > performance.max_participants):
                raise HTTPException(422, detail="Max participants exceeded")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'teacher': performance.teacher,
                'max_participants': performance.max_participants,
                'participants': performance.participants
            }

    # Update database
    data['performances'].append(perf)
    try:
        storage.update(data)
        response.status_code = status.HTTP_201_CREATED
        return perf
    except:
        raise HTTPException(500, detail="Failed to update database")


@app.put('/api/performances/{id}')
def edit_performance(performance: PerformanceModel, id: str):
    data = storage.data()

    # Get performance
    performances = [Performance(p) for p in data['performances']]
    target_perfs = list( filter(lambda x: x.id == id, performances))

    if (len(target_perfs) == 0):
        raise HTTPException(404, detail="Invalid performance id")
    target_perf = target_perfs[0]


    # Check venu
    venues: list[Venue]  = [Venue(venue) for venue in data['venues']]

    found_venue: None | Venue = None
    for v in venues:
        if (v.slug == performance.venue):
            found_venue = v
    if (not found_venue):
        raise HTTPException(404, detail="Invalid venue")

    # Check date format
    if (not parse(performance.start)):
        raise HTTPException(422, detail="Invalid date format")

    all_acts = [Artist(artist).slug for artist in data['artists']]
    perf: None | dict = None
    # Check by case
    match (performance.kind):
        case 'lineup':
            if (not performance.host or not performance.acts):
                raise HTTPException(422, detail="host and acts fields required for lineup kind")
            # Verify host and acts
            for act in performance.acts:
                if (not (act in all_acts)):
                    raise HTTPException(404, detail="Invalid act")
            if (not (performance.host in all_acts)):
                raise HTTPException(404, detail="Invalid act")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'host': performance.host,
                'acts': performance.acts
            }
        case 'solo':
            if (not performance.min_age or not performance.artist):
                raise HTTPException(422, detail="min_age and artist field required for solo kind")
            if (performance.min_age < 0):
                raise HTTPException(422, detail="Invalid min_age field")
            if (not (performance.artist in all_acts)):
                raise HTTPException(404, detail="Invalid artist field")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'artist': performance.artist,
                'min_age': performance.min_age
            }
        case 'workshop':
            if ((not performance.teacher) or (not performance.max_participants) or (not performance.participants)):
                raise HTTPException(422, detail="teacher, max_participants and participants fields are required")
            if (not (performance.teacher in all_acts)):
                raise HTTPException(404, detail="Invalid teacher")
            if (performance.max_participants == 0):
                raise HTTPException(422, detail="max_participants field must be positive")
            if (len(performance.participants) > performance.max_participants):
                raise HTTPException(422, detail="Max participants exceeded")
            perf = {
                'kind': performance.kind,
                'title': performance.title,
                'venue': performance.venue,
                'description': performance.description,
                'start': performance.start,
                'duration_minutes': performance.duration_minutes,
                'teacher': performance.teacher,
                'max_participants': performance.max_participants,
                'participants': performance.participants
            }

    # Update database
    target_perf.update(perf)
    newPerformances = list(filter(lambda x: x.id != id, performances))
    newPerformances.append(target_perf)
    data['performances'] = [p.dumbs() for p in newPerformances]
    
    try:
        storage.update(data)
        return perf
    except Exception as e:
        logError(e, 'Database update error')


@app.delete('/api/performances/{id}')
def delete_performance(id: str, response: Response):
    data = storage.data()
    performances = [Performance(performance) for performance in data['performances']]

    target: None | Performance = None
    for p in performances:
        if (p.id == id):
            target = p
            break
    if (not target):
        raise HTTPException(404, detail="Performance not found")
    newPerformances = list(filter (lambda p: p.id != id, performances))

    data['performances'] = [p.dumbs() for p in newPerformances]

    try:
        storage.update(data)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(500, detail="Failed to update database")



    
    

##### Serve frontend
app.frontend('/', directory='web/public/')
app.frontend('/admin', directory='web/admin/')