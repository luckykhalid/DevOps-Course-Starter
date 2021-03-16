"""This class represents single item object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    status: str
