"""Date fixtures."""

from datetime import date, timedelta

import pytest


@pytest.fixture
def today() -> date:
    """Provide the today date."""
    return date.today()


@pytest.fixture
def tomorrow() -> date:
    """Provide the tomorrow date."""
    return date.today() + timedelta(days=1)


@pytest.fixture
def later() -> date:
    """Provide the later date."""
    return date.today() + timedelta(days=2)
