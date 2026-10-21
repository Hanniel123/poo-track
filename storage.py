from config import *
from utils import *
import json

class Storage:
    
    def __init__(self):
        self._data = parse_file(DATABASE_FILE)

    def update(self, data: dict):
        self._data = data
        
        write_in_file(DATABASE_FILE, json.dumps(data, indent=2, ensure_ascii=False))

    def data(self):
        return self._data
