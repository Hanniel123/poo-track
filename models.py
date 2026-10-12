from utils import *

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
        self.end = data['end']
        self.duration_minutes = data['duration_minutes']

    @property
    def id(self):
        formatted_time = ''.join(self.start[11:].split(':'))
        return f'{turn_name_to_slug(self.title)}-{self.start[:10]}-{formatted_time}'

    @property
    def venue_name(self):
        return turn_slug_to_name(self.venue)

    @property
    def festival_day(self):
        return get_festival_day(self.start)[:10]

    @property
    def summary(self):
        pass

    def artists(self):
        pass

    def serialize(self):
        pass
    