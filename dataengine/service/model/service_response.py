import typing as t
from dataclasses import dataclass


@dataclass
class ServiceResponse:
    result: t.Any
    success: bool
    error_msg: str
