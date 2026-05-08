from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Command:
    verb: Optional[str] = None
    object_name: Optional[str] = None
    location: Optional[str] = None
    date: Optional[str] = None
    query: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[str] = None
    title: Optional[str] = None
    raw: str = ""
    errors: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, raw: str = "") -> "Command":
        return cls(
            verb=data.get('verbs'),
            object_name=data.get('objects'),
            location=data.get('location'),
            date=data.get('date'),
            query=data.get('query'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            duration=data.get('duration'),
            title=data.get('title'),
            raw=raw,
        )

    def to_dict(self) -> dict:
        result = {
            'verbs': self.verb,
            'objects': self.object_name,
            'location': self.location,
            'date': self.date,
            'query': self.query,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'title': self.title,
        }
        return {k: v for k, v in result.items() if v is not None}
