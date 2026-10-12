"""Stations along an edge: where a row of connectors, latches, brackets,
hinges or catches goes, spread evenly between two end offsets.

One rule for every add-in and the modeling language: `count` stations
along a stretch `length` long, the first and last `end` from its ends and
the rest evenly spaced between them; a single station sits in the middle,
whatever `end` says. Whether the stretch is long enough for `end`, and
which end offsets are allowed, is each caller's own rule
(`connector_data.stations`, `door_latches.stations`,
`sliding_brackets.stations` keep theirs).

Plain Python without Fusion imports, unit-free; `python3 -m lib.stations`
runs its self-checks.
"""


def stations(length: float, count: int, end: float) -> list[float]:
    """Distances from the start of a stretch `length` long: `count`
    stations, the first and last `end` from its ends and the rest evenly
    spaced between them; one station in the middle. Raises ValueError for
    no station."""
    if count < 1:
        raise ValueError("At least one station is needed.")
    if count == 1:
        return [length / 2]
    spacing = (length - 2 * end) / (count - 1)
    return [end + index * spacing for index in range(count)]


def _self_check() -> None:
    assert stations(100, 1, 10) == [50]
    assert stations(100, 1, 0) == [50]                    # one station: the end offset is not used
    assert stations(100, 3, 10) == [10, 50, 90]
    assert stations(566, 2, 80) == [80, 486]
    assert stations(500, 3, 100) == [100, 250, 400]
    # the same floats as the copies it replaces: end + index * spacing
    for length, count, end in ((597.0, 2, 60.0), (566.0, 3, 80.0), (1234.5, 7, 33.3)):
        spacing = (length - 2 * end) / (count - 1)
        assert stations(length, count, end) == [end + spacing * i for i in range(count)]
    try:
        stations(100, 0, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("no station")
    print("stations: all checks passed")


if __name__ == "__main__":
    _self_check()
