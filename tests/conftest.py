"""Every test starts from a fresh build: an empty registry and the default
world frame (`registry.reset()` restores both), and leaves one behind.

The fuzz tests (tests/fuzz) run a small fixed set of examples in every run
(profile `fast`, the same examples each time) and many random ones on
demand: `pytest tests/fuzz --hypothesis-profile=long`, which keeps the
failures it finds in .hypothesis/ and tries them first next time."""
from collections.abc import Iterator

import pytest
from hypothesis import HealthCheck, settings

from lang.core import directions
from lang.core.scope import registry

# A fuzz test resets the registry for each example itself (`fuzzing.fresh`),
# so the function-scoped fixture below is no concern of Hypothesis.
_QUIET = [HealthCheck.function_scoped_fixture, HealthCheck.too_slow, HealthCheck.filter_too_much]
settings.register_profile("fast", max_examples=25, deadline=None, derandomize=True, print_blob=True,
                          suppress_health_check=_QUIET)
settings.register_profile("long", max_examples=2000, deadline=None, print_blob=True, suppress_health_check=_QUIET)
settings.load_profile("fast")


@pytest.fixture(autouse=True)
def fresh_registry() -> Iterator[None]:
    registry.reset()
    yield
    registry.reset()
    assert repr(directions.frame) == repr(directions.Frame()), "a test left a world frame behind"
