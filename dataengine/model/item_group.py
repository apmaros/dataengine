import typing as t
from dataclasses import dataclass


@dataclass
class ItemGroup:
    """
    Groups items sharing the same characteristic defined by the key
    """
    key: str
    value: t.List[t.Any]

    def is_empty(self):
        return not self.value
