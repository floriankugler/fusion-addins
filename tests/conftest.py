"""Every test starts from a fresh build: an empty registry and the default
world frame (`registry.reset()` restores both), and leaves one behind."""
from collections.abc import Iterator

import pytest

from lang.core import directions
from lang.core.scope import registry


@pytest.fixture(autouse=True)
def fresh_registry() -> Iterator[None]:
    registry.reset()
    yield
    registry.reset()
    assert repr(directions.frame) == repr(directions.Frame()), "a test left a world frame behind"
