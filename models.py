from utils import *
from datetime import timedelta
import math
# from typing import Optional
# from pydantic import BaseModel

class Artist:

    def __init__(self, data: dict):
        self.name = data['name']
        self.bio = data['bio']
        self.photo_url = data['photo_url']

    @property
    def slug(self):
        return turn_name_to_slug(self.name)

    def serialize(self):
        return {
            'name': self.name,
            'bio': self.bio,
            'photo_url': self.photo_url,
            'slug': self.slug
        }


class Performance:
    def __init__(self, data: dict):
        self.kind = data['kind']
        self.title = data['title']
        self.venue = data['venue']
        self.start = data['start']

        self.duration_minutes = data['duration_minutes']
        self.description = data['description']

        match (self.kind):
            case 'solo':
                self.artist = data['artist']
                self.min_age = data['min_age']

            case 'lineup':
                self.host = data['host']
                self.acts = data['acts']
            case 'workshop':
                self.teacher = data['teacher']
                self.max_participants = data['max_participants']
                self.participants = data['participants']

        

    @property
    def id(self):
        formatted_time = ''.join(self.start[11:].split(':'))
        return f'{turn_name_to_slug(self.title)}-{self.start[:10]}-{formatted_time}'

    @property
    def end(self):
        date = datetime.fromisoformat(self.start)
        
        date = date + timedelta(minutes=int(self.duration_minutes))
        return date.isoformat(timespec='minutes')
    @property
    def venue_name(self):
        return turn_slug_to_name(self.venue)

    @property
    def festival_day(self):
        return get_festival_day(self.start)[:10]

    @property
    def summary(self):
        match self.kind:
            case 'solo':
                return turn_slug_to_name(self.artist)
            case 'lineup':
                return f"Hosted by {turn_slug_to_name(self.host)}, with {" ".join(turn_slug_to_name(act) for act in self.acts)}"
            case 'workshop':
                return self.teacher
        return ""

    @property
    def places_left(self):
        if (self.kind == 'workshop'):
            return max(0, self.max_participants - len(self.participants))
        return None

    @property
    def artists(self):
        return []

    def serialize(self):
        response = {
            'id': self.id,
            'kind': self.kind,
            'title': self.title,
            'venue': self.venue,
            'venue_name': self.venue_name,
            'start': self.start,
            'end': self.end,
            'duration_minutes': self.duration_minutes,
            'festival_day': self.festival_day,
            'description': self.description,
            'summary': self.description,
            'artists': self.artists
        }
        if (self.kind == 'workshop'):
            response['capacity'] = self.max_participants
        return response
    