"""This class represents single item object."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    status: str
    date_last_activity: datetime
