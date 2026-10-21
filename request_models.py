from pydantic import BaseModel
from typing import Literal

class ArtistModel(BaseModel):
    name: str
    bio: str | None = ""
    photo_url: str | None = ""



class PerformanceModel(BaseModel):
    kind: Literal["lineup", "solo", "workshop"]
    title: str
    venue: str
    start: str
    description: str | None = ""
    duration_minutes: int
    host: str | None = None # lineup
    acts: list[str] | None = None # lineuop
    teacher: str | None = None # workshop
    max_participants: int | None = None # Workshop
    participants: list[str] | None = None # Workshop
    artist: str | None = None # solo
    min_age: int | None = None # solo

class ParticipantModel(BaseModel):
    name: str
