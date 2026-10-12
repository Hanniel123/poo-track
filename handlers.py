from utils import *

def get_festival_days(performances: list[dict])->list[str]:
    days: set = set()
    for pf in performances:
        # days.
        days.add(pf['start'][:10])
    return sorted(days)

def serialize_venues(venues: list[dict] | dict):
    if (isinstance(venues, dict)):
        return {
            'slug': turn_name_to_slug(venue['name']),
            'name': venue['name'],
            'capacity': venue['capacity'],
            'address': venue['address']
        }
    serialized_venues = []
    for venue in venues:
        serialized_venues.append({
            'slug': turn_name_to_slug(venue['name']),
            'name': venue['name'],
            'capacity': venue['capacity'],
            'address': venue['address']
        })
    return serialized_venues

