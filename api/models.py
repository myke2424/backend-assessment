from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class BlogPost:
    id: int
    author: str
    author_id: int
    likes: int
    popularity: float
    reads: int
    tags: List[str]

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "author": self.author,
            "authorId": self.author_id,
            "likes": self.likes,
            "popularity": self.popularity,
            "reads": self.reads,
            "tags": self.tags,
        }
