"""API tests."""

import pytest


@pytest.mark.usefixtures('restart_api')
def test_api_returns_allocation(add_stock) -> None:  # type: ignore
    pass
