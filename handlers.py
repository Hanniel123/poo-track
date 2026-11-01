from utils import *
from fastapi import HTTPException
from models import Performance, Artist

def get_festival_days(performances: list[dict])->list[str]:
    days: set = set()
    for pf in performances:
        # days.
        days.add(pf['start'][:10])
    return sorted(days)

def logError(e: Exception, prefix: str= "Exception caught"):
    print(f'{prefix}: {e}')
    raise HTTPException(500, f'{prefix}: {e}')

def get_artist_performances(performances: list[Performance], artist: Artist):
    result = [p for p in performances if ((p.kind == 'solo' and p.artist == artist.name) or (p.kind == 'lineup' and p.host == artist.name) or (p.kind == 'lineup' and p.acts.count(turn_name_to_slug(artist.name)) > 0) or (p.kind == 'workshop' and p.teacher == artist.name))  ]
    result.sort(key=lambda x: x.start)
    return [p.serialize() for p in result]

