from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Genre:
    genreName: str

@dataclass
class Actor:
    fullName: str

@dataclass
class Review:
    ratingStars: int
    reviewText: str

@dataclass
class Episode:
    episodeTitle: str
    durationSeconds: int

@dataclass
class Season:
    seasonNumber: int
    episodes: List[Episode]

@dataclass
class Title:
    name: str
    releaseYear: int
    genres: List[Genre]
    actors: List[Actor]
    reviews: List[Review]

    def playMedia(self) -> bool:
        pass

@dataclass
class Film(Title):
    lengthMinutes: int

@dataclass
class TVShow(Title):
    seasonsCount: int
    seasons: List[Season]
