"""Pytest configuration."""

from datetime import date, timedelta

import pytest


@pytest.fixture
def today() -> date:
    """Provide today date."""
    return date.today()


@pytest.fixture
def tomorrow() -> date:
    """Provide tomorrow date."""
    return date.today() + timedelta(days=1)


@pytest.fixture
def later() -> date:
    """Provide later date."""
    return date.today() + timedelta(days=2)
