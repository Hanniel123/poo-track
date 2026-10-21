from utils import *
from fastapi import HTTPException

def get_festival_days(performances: list[dict])->list[str]:
    days: set = set()
    for pf in performances:
        # days.
        days.add(pf['start'][:10])
    return sorted(days)

def logError(e: Exception, prefix: str= "Exception caught"):
    print(f'{prefix}: {e}')
    raise HTTPException(500, f'{prefix}: {e}')
