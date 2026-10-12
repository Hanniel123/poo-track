import json
from datetime import datetime

def parse_file(file: str)-> dict:
    f = open(file)
    file_content = f.read()
    f.close()
    return json.loads(file_content)

def turn_name_to_slug(name: str)->str:
    return "-".join(name.lower().split(' ')).replace('é', 'e').replace('è', 'e')

def turn_slug_to_name(slug: str)->str:
    return " ".join([(v[0].upper() + v[1:]).replace('e', 'e') for v in slug.split('-')])

def get_festival_day(original_date: str)-> str:
    parsed_date = datetime.fromisoformat(original_date)

    if (parsed_date.hour < 6 and parsed_date.hour >= 0):
        parsed_date = parsed_date.replace(day=parsed_date.day - 1)
    return parsed_date.isoformat()

