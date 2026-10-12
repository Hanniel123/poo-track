import json
import sys
from datetime import datetime, date, timedelta
# imdateutil

DATA_FILE = 'data/festival.json'


def step_zero(data):
    print(data['name'])
    print(f"From {data['first_day']} to {data['last_day']}")
    print(f"{len(data['venues'])} venues, {len(data['artists'])} artists, {len(data['performances'])} performances")

def first_step(data):
    # Venues
    total_seats = 0
    print('Venues:')
    for venue in data['venues']:
        print(f"- {venue['name']}: {venue['capacity']} seats ({venue['address']})")
        total_seats += venue['capacity']
    print(f"Total: {total_seats} seats")

    performances: list[dict] = data['performances']
    
    # Performances at Le Kiosque
    print("At Le Kiosque:")
    for performance in performances:
        print(f"- {performance['start']} {performance['title']}")

    # Longest performance
    toSort = performances
    def predicate(e: dict):
        return e['duration_minutes']
    toSort.sort(key=predicate)
    # print(toSort)
    longest_performance = toSort[-1]
    print(f"\nLongest: {longest_performance['title']} ({longest_performance['duration_minutes']} min)\n")
    # Performances
    for p in performances:
        pass
        if (p['kind'] != 'workshop'):
            continue
        print(f"{p['title']} on {p['start']}: {len(p['participants'])}/{p['max_participants']}")

def second_step(data, cmd: str):
    # date_regex = '\d-\d-\d'
    # while True:
        # cmd = input("Day (YYYY-MM-DD): ")
        # found = re.search(date_regex, cmd)
        founds: list[dict] = []
        if (len(cmd) != 10):
            print(f"No performance on '{cmd}'")
            return
        for p in data['performances']:
            date = p['start'][:10]
            if (date == cmd):
                founds.append(p)
        if (len(founds) > 0):
            print(f"Programme for {cmd}")
        for p in founds:
            venue = turn_slug_to_name(p['venue'])
            print(f"{p['start'][11:]} | {venue} | {p['title']} ({p['kind']})")

def turn_name_to_slug(name: str)->str:
    return "-".join(name.split(' ')).replace('é', 'e').replace('è', 'e')

def turn_slug_to_name(slug: str)->str:
    return " ".join([(v[0].upper() + v[1:]).replace('e', 'e') for v in slug.split('-')])

def parse_file():
    f = open(DATA_FILE)
    file_content = f.read()
    f.close()
    return json.loads(file_content)

def get_venues(data):
    for v in data['venues']:
        slug = turn_name_to_slug(v['name'])
        print(f"{slug}: {v['name']}, {v['capacity']} seats")
# act = ['a', 'b']
# act.coun
def get_performances(data: dict, artist: str):
    artist_performances: list[dict] = []
    performances: list[dict] = data['performances']
    # artist_performances.
    for pf in performances:
        if (pf.__contains__('acts') and pf['acts'].count(artist) != 0):
            pf['role'] = 'act'
            artist_performances.append(pf)
        elif (pf.__contains__('artist') and pf['artist'] == artist and pf['kind'] == 'solo'):
            pf['role'] = 'solo'
            artist_performances.append(pf)
        elif (pf.__contains__('teacher') and pf['teacher'] == artist):
            pf['role'] = 'teacher'
            artist_performances.append(pf)
        elif (pf.__contains__('host') and pf['host'] == artist):
            pf['role'] = 'host'
            artist_performances.append(pf)

    if (len(artist_performances) > 0):
        print(turn_slug_to_name(artist))
    for p in artist_performances:
        print(f"{p['start'][:10]} {p['start'][11:]} | {turn_slug_to_name(p['venue'])} | {p['title']} ({p['role']})")

# def main():
#     try:
#         dat = date.fromisoformat(sys.argv[1])
#         print(timedelta(dat))
#         # print(datetime.fromisoformat(sys.argv[1]))
#         # data = parse_file()
#         # if (len(sys.argv) == 1):
#         #     step_zero(data)
#         #     return
#         # if (sys.argv[1] == 'venues'):
#         #     get_venues(data)
#         # if (len(sys.argv) == 3 and sys.argv[1] == 'artist'):
#         #     get_performances(data, sys.argv[2])
#         # if (len(sys.argv) == 3 and sys.argv[1] == 'programme'):
#         #     second_step(data, sys.argv[2])
#         # # Step zero
#         # # step_zero(data)

#         # # first_step(data)
#         # second_step(data)

#     except Exception as e:
#         print(f"Something went wrong {e}")
    

# if __name__ == "__main__":
#     main()
