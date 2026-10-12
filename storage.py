from config import *
from utils import *

class Storage:
    
    def __init__(self):
        self.data = parse_file(DATABASE_FILE)
    
