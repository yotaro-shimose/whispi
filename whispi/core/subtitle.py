from dataclasses import dataclass


@dataclass
class Subtitle:
    text: str
    start_sec: float
    end_sec: float
