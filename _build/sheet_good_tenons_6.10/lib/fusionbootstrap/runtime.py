from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeInfo:
    dev_mode: bool
    version: str
    id: str
